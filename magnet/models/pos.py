# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import math

import logging
_logger = logging.getLogger(__name__)





class PosConfig(models.Model):
    
    _inherit = 'pos.config'


    gps_latitude = fields.Float(u'Latitude', digits=(12,15))
    gps_longitude = fields.Float(u'Longitude', digits=(12,15))
    code = fields.Char(u'Pos Code')


    def search_from_gps_position(self, latitude, longitude):
        R = 6372800 # Föld sugara
        D = 20000000 # Föld kerületének a fele kb. a távolságot innen kezdjük nézni
        id = 0
        for pos in self.env['pos.config'].search([]):
            phi1 = math.radians(latitude)
            phi2 = math.radians(pos.gps_latitude) 
            dphi = math.radians(pos.gps_latitude - latitude)
            dlambda = math.radians(pos.gps_longitude - longitude)
            a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
            distance = 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
            if distance < D:
                D = distance
                id = pos.id
        return id
