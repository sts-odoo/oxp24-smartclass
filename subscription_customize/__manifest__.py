{
    'name': 'Module to upgrade',
    'version': '0.2',
    'summary': 'A module extending subscription in 15.0 to upgrade',
    'description': '',
    'sequence': 1,
    'author': 'Odoo S.A.',
    'website': 'http://www.odoo.com',
    'depends': ['sale_subscription'],
    'data': [
        'views/subscription.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
