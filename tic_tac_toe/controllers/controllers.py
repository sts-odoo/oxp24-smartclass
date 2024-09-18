# -*- coding: utf-8 -*-
import logging

from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


_logger = logging.getLogger(__name__)


class TicTacToe(CustomerPortal):

    @http.route('/my/tictactoe/<int:game_id>', type='http', auth='public', website=True)
    def portal_my_game(self, game_id=None, access_token=None, **kw):
        try:
            game_sudo = self._document_check_access('tictactoe.game', game_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        return request.render("tic_tac_toe.portal_my_game", {'game': game_sudo})

    @http.route(['/my/tictactoe/games', '/my/tictactoe/games/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_games(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        Game = request.env['tictactoe.game']
        domain = []

        searchbar_filters = {
            'my': {'label': _('My games'), 'domain': ['|', ('player_x_id', '=', request.env.user.id), ('player_o_id', '=', request.env.user.id)]},
            'open': {'label': _('Open games'), 'domain': [('is_open', '=', True)]},
            'all': {'label': _('All'), 'domain': [('is_open', '=', False)]},
        }
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if not filterby:
            filterby = 'my'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        game_count = Game.search_count(domain)
        pager = portal_pager(
            url="/my/tictactoe/games",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=game_count,
            page=page,
            step=self._items_per_page
        )
        games = Game.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'games': games,
            'page_name': 'games',
            'default_url': '/my/tictactoe/games',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("tic_tac_toe.portal_my_games", values)

    @http.route(['/tictactoe/initialize'], auth='user')
    def initialize(self, **kw):
        game_id = request.env['tictactoe.game']._initialize()
        return request.redirect('/my/tictactoe/%s' % game_id.id)

    @http.route(['/tictactoe/<model("tictactoe.game"):game_id>/join'], auth='user')
    def join(self, game_id, **kw):
        game_id._join()
        return request.redirect('/my/tictactoe/%s' % game_id.id)

    @http.route(['/tictactoe/<model("tictactoe.game"):game_id>/play'], auth='user', type='json')
    def play(self, game_id, position, **kw):
        game_id._play(position)
        return game_id.current_state()
