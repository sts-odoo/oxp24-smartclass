# -*- coding: utf-8 -*-
import logging

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError


_logger = logging.getLogger(__name__)


class Syncstuff(http.Controller):

    @http.route('/pull/single/<int:record_id>', type='http', auth='public')
    def pull_single(self, record_id=None, access_token=None, **kw):
        return request.env['sale.order'].sudo()._get_data(rec_id=record_id)

    @http.route('/pull/all', type='http', auth='public')
    def pull_all(self, limit=100, **kw):
        return request.env['sale.order'].sudo()._get_data(limit=limit)

    @http.route('/push/<string:sync_type>', type='http', auth='public')
    def push_data(self, sync_type, url, token=None, **kw):
        if sync_type not in ['single', 'all']:
            return 'Type must be either "single" or "all"'
        sync_stuff = request.env['sync.stuff'].sudo()
        already_sync_stuff = sync_stuff.search([('url', '=', url), ('state', '=', 'draft')])
        if already_sync_stuff:
            return 'Already got stuff to sync'
        vals = {
            'url': url,
            'sync_type': sync_type,
        }
        if token:
            vals['token'] = token
        if 'limit' in kw:
            kw['limit'] = kw['limit']
        sync_stuff.create(vals)
        request.env.ref('sync_source.cron_sync_stuff').sudo()._trigger()
        return 'ok'

