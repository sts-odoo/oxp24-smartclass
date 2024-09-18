# -*- coding: utf-8 -*-
import logging
from werkzeug.exceptions import Forbidden

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError


_logger = logging.getLogger(__name__)

class Syncstuff(http.Controller):

    @http.route('/sync_incoming', type='http', auth='none', csrf=False, cors='*')
    def sync_incoming(self, record_id=None, access_token=None, **kw):
        if not access_token:
            raise Forbidden()
        if access_token != request.env['ir.config_parameter'].sudo().get_param('token'):
            raise Forbidden()
        sync_stuff = request.env['sync.stuff'].sudo()
        sync_stuff.create({'data': kw.get('data')})
        request.env.ref('sync_source.cron_sync_stuff').sudo()._trigger()
