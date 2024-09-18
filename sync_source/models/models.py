# -*- coding: utf-8 -*-
import logging
import json
import requests

from odoo import models, api, fields
from odoo.exceptions import ValidationError
from odoo.addons.base.populate.res_company import Partner

_logger = logging.getLogger(__name__)


def new_company_populate(self, size):
    return self.env['res.company'].search([])


Partner._populate = new_company_populate


class sync(models.Model):
    _description = "source sync"
    _inherit = "sale.order"

    def _get_data(self, rec_id=None, limit=100):
        domain = []
        if rec_id:
            domain = [('id', '=', rec_id)]
        res = []
        for so in self.env['sale.order'].search(domain, limit=limit):
            res.append({
                'identifier': so.id,
                'name': so.name,
                'partner_identifier': so.partner_id.id,
                'partner_name': so.partner_id.name,
                'lines': [{
                    'product_identifier': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.product_uom_qty,
                    } for line in so.order_line],
            })
        return json.dumps(res)


class stuff(models.Model):
    _description = "source sync stuff"
    _name = "sync.stuff"

    url = fields.Char()
    token = fields.Char()
    limit = fields.Integer(default=100)
    sync_type = fields.Selection([
        ('single', 'Single'),
        ('all', 'All'),
        ], default='all')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'Progress'),
        ('done', 'Done'),
        ('failed', 'Failed'),
        ], default='draft')

    def _cron_handle_sync(self):
        sync = self.search([('state', '=', 'draft')], limit=1)
        sync.state = 'progress'
        if not sync:
            return
        try:
            recs = self.env['sale.order'].sudo()._get_data(limit=sync.limit)
            if sync.sync_type == 'all':
                data = {'data': recs}
                if sync.token:
                    data['token'] = sync.token
                    data['access_token'] = sync.token
                requests.post(sync.url, data=data, timeout=10)
            else:
                for rec in recs:
                    data = {'data': rec}
                    if sync.token:
                        data['token'] = sync.token
                        data['access_token'] = sync.token
                    requests.post(sync.url, data=data, timeout=10)
        except Exception:
            _logger.exception('Failed to sync to %s', sync.url)
            sync.state = 'failed'
        sync.state = 'done'
        next_sync = self.search([('state', '=', 'draft')], limit=1)
        if next_sync:
            self.env.ref('sync_source.cron_sync_stuff').sudo()._trigger()
