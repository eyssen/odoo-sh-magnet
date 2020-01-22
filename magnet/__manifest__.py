# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Magnet',
    'version' : '1.0',
    'summary': 'Magnet Addon',
    'sequence': 15,
    'description': """
Magnet Addon
    """,
    'category': 'Other',
    'website': 'https://www.eyssen.hu',
    'depends' : ['point_of_sale'],
    'data': [
        'views/pos.xml',
        'views/product.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
