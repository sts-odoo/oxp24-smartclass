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
    end = fields.Datetime(compute='_compute_end', store=True)
    winner_id = fields.Many2one('res.users', string="Winner", compute='_compute_winner', store=True)
    next_player_id = fields.Many2one('res.users', string="Next Player", compute='_compute_next_player')
    is_open = fields.Boolean(compute='_compute_is_open', store=True)
    play_ids = fields.One2many('tictactoe.play', 'game_id')

    @api.constrains('player_x_id', 'player_o_id')
    def _check_player(self):
        for rec in self:
            if rec.player_x_id == rec.player_o_id:
                raise ValidationError("You cannot play against yourself")

    @api.depends('player_o_id.name', 'player_x_id.name')
    def _compute_name(self):
        for rec in self:
            players = rec.player_o_id | rec.player_x_id
            if not players:
                rec.name = 'OPEN GAME'
            elif len(players) == 1:
                rec.name = 'OPEN GAME (vs %s)' % players.name
            else:
                rec.name = '%s vs %s' % (rec.player_x_id.name, rec.player_o_id.name)

    @api.depends('play_ids.position', 'play_ids.game_id')
    def _compute_winner(self):
        for rec in self:
            rec.winner_id = False
            for player in [rec.player_x_id, rec.player_o_id]:
                all_positions = set(rec.play_ids.filtered(lambda r: r.player_id == player).mapped('position'))
                for position in WINNING_COORDINATE:
                    if position.issubset(all_positions):
                        rec.winner_id = player

    @api.depends('play_ids.sequence', 'winner_id')
    def _compute_end(self):
        for rec in self:
            if rec.winner_id or len(rec.play_ids) == 9:
                rec.end = fields.Datetime.now()
            else:
                rec.end = False

    @api.depends('play_ids', 'winner_id')
    def _compute_next_player(self):
        for rec in self:
            rec.next_player_id = rec.player_x_id
            if rec.play_ids[-1:]:
                if rec.play_ids[-1:].player_id == rec.player_x_id:
                    rec.next_player_id = rec.player_o_id
                else:
                    rec.next_player_id = rec.player_x_id
            if rec.winner_id:
                rec.next_player_id = False

    @api.depends('player_o_id', 'player_x_id')
    def _compute_is_open(self):
        for rec in self:
            rec.is_open = len(rec.player_o_id | rec.player_x_id) != 2

    def _play(self, position):
        self.ensure_one()
        self.play_ids.create({
            'game_id': self.id,
            'position': position,
        })

    def _join(self):
        self.ensure_one()
        if not self.player_x_id:
            self.player_x_id = self.env.user
        elif not self.player_o_id:
            self.player_o_id = self.env.user
        else:
            raise ValidationError("The game is already full")

    @api.model
    def _initialize(self):
        game = self.create({})
        game._join()
        return game

    def current_state(self):
        self.ensure_one()
        result = self.read()[0]
        result['play_ids'] = self.play_ids.read()
        return result

class TicTacToePlay(models.Model):
    _description = "Tic Tac Toe Play"
    _name = "tictactoe.play"

    sequence = fields.Integer(default=1)
    game_id = fields.Many2one('tictactoe.game', ondelete='cascade', required=True)
    player_id = fields.Many2one('res.users', 'Player', default=lambda self: self.env.user, required=True)
    position = fields.Selection([
        ('1', 'Top Left'),
        ('2', 'Top Center'),
        ('3', 'Top Right'),
        ('4', 'Middle Left'),
        ('5', 'Middle Center'),
        ('6', 'Middle Right'),
        ('7', 'Bottom Left'),
        ('8', 'Bottom Center'),
        ('9', 'Bottom Right'),
        ], required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('game_id'):
                last_play = self.game_id.browse(vals['game_id']).play_ids[-1:]
                if last_play:
                    vals['sequence'] = last_play.sequence + 1
        res = super().create(vals_list)
        self.env["bus.bus"]._sendone(
                    str(res.game_id.id),
                    "tic_tac_toe",
                    {res.position: 'X' if res.player_id == res.game_id.player_x_id else 'O'},
                )
        return res

    @api.constrains('player_id', 'sequence', 'game_id', 'position')
    def _check_player(self):
        for rec in self:
            last_play_ids = rec.game_id.play_ids[-2:]
            # if rec.player_id != self.env.user:
            #     raise ValidationError("You can only play for yourself")
            if rec.player_id not in [rec.game_id.player_x_id, rec.game_id.player_o_id]:
                raise ValidationError("Are you trying to play on someone else's game")
            if len(last_play_ids) == 1 and last_play_ids.player_id != rec.game_id.player_x_id:
                raise ValidationError("The first player should be the X player")
            if len(last_play_ids) == 2 and len(last_play_ids.player_id) != 2:
                raise ValidationError("One at a time pretty please")
            if len(set(rec.game_id.play_ids.mapped('position'))) < len(rec.game_id.play_ids.mapped('position')):
                raise ValidationError("You cannot play on a previously used position")
