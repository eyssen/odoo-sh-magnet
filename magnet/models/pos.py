# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)





class PosConfig(models.Model):
    
    _inherit = 'pos.config'


    gps_latitude = fields.Float(u'Latitude')
    gps_longitude = fields.Float(u'Longitude')
