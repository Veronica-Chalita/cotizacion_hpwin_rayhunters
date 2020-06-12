# -*- coding: utf-8 -*-
{
    'name': 'Comercializadora Proxima',
    'summary': 'Comercializadora Proxima',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.1',
    'author': 'Odoo Inc',
    'description': """
Comercializadora Proxima: Multiple Currency
===============================
*[#2260071]
    - currency rate value on SO, company currency value on SO Line
    - pass product unit price (company currency) to invoice 
    """,
    'category': 'Custom Development',

    # any module necessary for this one to work correctly
    'depends': ['sale','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}