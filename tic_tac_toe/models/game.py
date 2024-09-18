# -*- coding: utf-8 -*-
import logging

from odoo import models, api, fields
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

WINNING_COORDINATE = [
    set(['1', '2', '3']),
    set(['4', '5', '6']),
    set(['7', '8', '9']),
    set(['1', '4', '7']),
    set(['2', '5', '8']),
    set(['3', '6', '9']),
    set(['1', '5', '9']),
    set(['7', '5', '3']),
]


class TicTacToeGame(models.Model):
    _description = "Tic Tac Toe Game"
    _name = "tictactoe.game"
    _inherit = ['website.published.mixin', 'mail.thread', 'portal.mixin']

    name = fields.Char(string="Name", compute='_compute_name', store=True)
    player_x_id = fields.Many2one('res.users', string="Player X")
    player_o_id = fields.Many2one('res.users', string="Player O")
    start = fields.Datetime(default=fields.Datetime.now, readonly=True)

class TicTacToePlay(models.Model):
    _description = "Tic Tac Toe Play"
    _name = "tictactoe.play"
