# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import math

import logging
import xxlimited
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





class PosOrder(models.Model):
    
    _inherit = 'pos.order'
    
    
    def create_from_app(self, pos_id):

        Session = self.env['pos.session'].search([('config_id', '=', pos_id), ('state', '=', 'opened')])
        if Session:
            
            Order = self.env['pos.order'].search([('session_id', '=', Session.id)], order='sequence_number desc', limit=1)
            if Order:
                sequence_number = Order.sequence_number + 1
            else:
                sequence_number = 1
            
            vals = {
                'session_id': Session.id,
                'state': 'draft',
                'to_invoice': False,
                'sequence_number': sequence_number,
                'name': self.env['ir.sequence'].browse(Session.config_id.sequence_id.id)._next(),
                'company_id': Session.company_id.id,
                'procelist_id': 1,
                'nb_print': 0,
                'pos_reference': 'Order ' + format(Session.id, '05d') + '-' + format(pos_id, '03d') + '-' + format(sequence_number, '04d'), #TODO: ezt lehet hogy máshogy kéne számolni
                'amount_tax': 0,
                'amount_total': 0,
                'amount_paid': 0,
                'amount_return': 0
            }
            Order = self.env['pos.order'].create(vals)
            return Order.id

        else:
            return 0
    
    
    def add_order_line(self, order_id, product_id, img):
        
        Order = self.env['pos.order'].search([('id', '=', order_id)], limit=1)
        Product = self.env['product.product'].search([('id', '=', product_id)], limit=1)
        if Order and Product:
            
            vals = {
                'company_id': Order.company_id.id,
                'name': self.env['ir.sequence'].browse(Order.session_id.config_id.sequence_line_id.id)._next(),
                'product_id': Product.id,
                'qty': 1,
                'price_unit': Product.list_price,
                'price_subtotal': Product.list_price,
                'price_subtotal_incl': Product.list_price * 1.27, #TODO: Ide bruttó ár kell!
                'order_id': Order.id,
                'discount': 0,
                'print_image': img
            }
            self.env['pos.order.line'].create(vals)
            
            Order.amount_tax = Product.list_price * 0.27 #TODO: Ide az ÁFA kell
            Order.amount_total = Product.list_price * 1.27
            Order.amount_paid = Product.list_price * 1.27 #TODO: Ezt majd a fizetéshez kell állítani
            
            return 1
            
        else:
            return 0


    def print_it_out(self, order_id):

        Order = self.env['pos.order'].search([('id', '=', order_id)], limit=1)
        
        if Order:
            Order.state = 'paid'
            return 1
        
        else:
            return 0





class PosOrderLine(models.Model):
    
    _inherit = 'pos.order.line'
    
    print_image = fields.Binary(u'Nyomtatási kép')
