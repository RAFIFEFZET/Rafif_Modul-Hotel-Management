from odoo import models, fields

class HotelServices(models.Model):
    _name = 'hotel.services'
    _description = 'Hotel Services'

    name = fields.Char(string='Service Name', required=True)
    price = fields.Float(string='Price', required=True)
