{
    'name': 'Dental Practice',
    'version': '0.1',
    'summary': 'A dental practice management',
    'description': '',
    'sequence': 1,
    'author': 'Odoo S.A.',
    'website': 'http://www.odoo.com',
    'depends': ['sale'],
    'data': [
        'views/dental.xml',
        'security/ir.model.access.csv'
    ],
    'assets': {
        'web.assets_backend': [
            'dental_practice/static/src/**/*',
        ],
    },
    'demo': [
        'data/dental_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3'
}
