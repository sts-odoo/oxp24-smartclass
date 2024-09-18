{
    'name': 'Tic Tac Toe',
    'version': '0.1',
    'summary': 'A multiplayer Tic Tac Toa game',
    'description': '',
    'sequence': 1,
    'author': 'Odoo S.A.',
    'website': 'http://www.odoo.com',
    'depends': ['base', 'portal', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/game.xml',
        'views/res_user.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'tic_tac_toe/static/src/**/*',
        ],
    },
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
