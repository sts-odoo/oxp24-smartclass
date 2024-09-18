# -*- coding: utf-8 -*-
import logging
import json
import requests

from odoo import models, api, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


BASE_URL = 'https://oxp24-smartclass-app.odoo.com'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sync_identifier = fields.Char('Indetifier on other system', index=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sync_identifier = fields.Char('Indetifier on other system', index=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sync_identifier = fields.Char('Indetifier on other system', index=True)

class stuff(models.Model):
    _description = "source sync stuff"
    _name = "sync.stuff"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Done'),
        ('failed', 'Failed'),
        ], default='draft')
    data = fields.Text()

    @api.model
    def _pull_data(self):
        data = requests.get(BASE_URL + '/pull/all')
        self.create({'data': data.content})
        self.env.ref('sync_source.cron_sync_stuff').sudo()._trigger()

    def _cron_handle_sync(self, batch=10):
        sync = self.search([('state', 'in', ['draft', 'progress'])], limit=1, order='state desc')
        if not sync:
            return
        data = json.loads(sync.data)
        i = 0
        try:
            while True:
                if not len(data):
                    break
                if i > batch:
                    break
                element = data.pop()
                sale_order_id = self.env['sale.order'].search([('sync_identifier', '=', element.get('identifier'))])
                partner_id = self.env['res.partner'].search([('sync_identifier', '=', element.get('partner_identifier'))])
                if not partner_id:
                    partner_id = self.env['res.partner'].create({
                        'name': element.get('partner_name'),
                        'sync_identifier': element.get('identifier'),
                    })
                elif partner_id.name != element.get('partner_name'):
                    partner_id.name = element.get('partner_name')
                if not sale_order_id:
                    sale_order_id = self.env['sale.order'].create({
                        'sync_identifier': element.get('identifier'),
                        'partner_id': partner_id.id,
                    })
                for line in element.get('lines', []):
                    product_id = self.env['product.template'].search([('sync_identifier', '=', element.get('partner_identifier'))])
                    if not product_id:
                        product_id = self.env['product.template'].create({
                            'name': line.get('product_name'),
                            'sync_identifier': element.get('product_identifier'),
                        })
                    so_line = sale_order_id.order_line.filtered(lambda r: r.product_id.id == product_id.id)
                    if so_line:
                        so_line.product_uom_qty = line.get('quantity', 0)
                    else:
                        self.env['sale.order.line'].create({
                            'order_id': sale_order_id.id,
                            'product_id': product_id.product_variant_id.id,
                            'product_uom_qty': line.get('quantity', 0),
                        })
                i += 1
            if data:
                sync.data = json.dumps(data)
            else:
                sync.data = False
                sync.state = 'done'
        except Exception:
            _logger.exception('Failed to sync to %s', sync.id)
            sync.state = 'failed'
        next_sync = self.search([('state', 'in', ['draft', 'progress'])], limit=1, order='state desc')
        if next_sync:
            self.env.ref('sync_source.cron_sync_stuff').sudo()._trigger()
