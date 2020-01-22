# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)





class ProductTemplate(models.Model):
    
    _inherit = 'product.template'


    print_image = fields.Binary(u'Nyomtatási kép')
    subimage_position_ax = fields.Float(u'Beillesztett kép pozíció (AX %)')
    subimage_position_ay = fields.Float(u'Beillesztett kép pozíció (AY %)')
    subimage_position_bx = fields.Float(u'Beillesztett kép pozíció (BX %)')
    subimage_position_by = fields.Float(u'Beillesztett kép pozíció (BY %)')
    pos_ids = fields.Many2many('pos.config', 'product_tmpl_pos_rel', 'product_tmpl_id', 'pos_id', string=u'Melyik terminálokon érhető el')
