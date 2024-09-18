# -*- coding: utf-8 -*-
import logging

from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


_logger = logging.getLogger(__name__)
