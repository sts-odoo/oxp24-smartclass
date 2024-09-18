# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import fields, models
import requests
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    wins = fields.Integer(string='Wins')
    losses = fields.Integer(string='Losses')
    ties = fields.Integer(string='Ties')
