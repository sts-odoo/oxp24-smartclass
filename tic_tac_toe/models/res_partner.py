# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import fields, models
import requests
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    wins = fields.Integer(string='Wins', compute='_compute_wins_losses')
    losses = fields.Integer(string='Losses', compute='_compute_wins_losses')
    ties = fields.Integer(string='Ties', compute='_compute_wins_losses')

    def _compute_wins_losses(self):
        game_ids = self.env['tictactoe.game'].search([
            ('end', '!=', False),
            '|',
                ('player_x_id', 'in', self.user_ids.ids),
                ('player_o_id', 'in', self.user_ids.ids),
        ])
        totals = defaultdict(lambda: {
            'wins': 0,
            'losses': 0,
            'ties': 0,
            })
        for game_id in game_ids:
            if game_id.winner_id:
                totals[game_id.winner_id.partner_id.id]['wins'] += 1
                loser_id = (game_id.player_x_id | game_id.player_o_id) - game_id.winner_id
                totals[loser_id.partner_id.id]['losses'] += 1
            else:
                totals[game_id.player_x_id.partner_id.id]['ties'] += 1
                totals[game_id.player_o_id.partner_id.id]['ties'] += 1
        for rec in self:
            rec.wins = totals[rec.id]['wins']
            rec.losses = totals[rec.id]['losses']
            rec.ties = totals[rec.id]['ties']
