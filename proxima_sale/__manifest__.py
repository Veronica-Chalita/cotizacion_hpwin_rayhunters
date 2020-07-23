# -*- coding: utf-8 -*-
{
    'name': 'Comercializadora Proxima: Multi Currency Quotations',
    'summary': 'Multi Currency rate on quotations to invoice',
    'sequence': 100,
    'license': 'OEEL-1',
    'website': 'https://www.odoo.com',
    'version': '1.1',
    'author': 'Odoo Inc',
    'description': """
    - currency rate value on SO, company currency value on SO Line
    - pass product unit price (company currency) to invoice 
    """,
    'category': 'Custom Development',

    # any module necessary for this one to work correctly
    'depends': ['sale','sale_management','account','account_accountant'],

    # always loaded
    'data': [
        'views/sale_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}