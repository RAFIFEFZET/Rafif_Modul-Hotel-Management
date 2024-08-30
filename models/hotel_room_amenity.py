from odoo import models, fields, api

class HotelRoomAmenity(models.Model):
    _name = 'hotel.room.amenity'
    _description = 'Hotel Room Amenity'

    room_id = fields.Many2one('hotel.room', string="Room", required=True, ondelete='cascade')
    amenity_id = fields.Many2one('hotel.amenity', string="Amenity", required=True)
    product_id = fields.Many2one('product.product', related='amenity_id.product_id', string="Related Product", readonly=True)
    quantity = fields.Integer(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price", related='product_id.list_price', readonly=True)
    total_price = fields.Float(string="Total Price", compute='_compute_total_price', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.quantity * record.price_unit

    @api.model
    def create(self, vals):
        if 'room_id' not in vals and self.env.context.get('default_room_id'):
            vals['room_id'] = self.env.context['default_room_id']
        return super(HotelRoomAmenity, self).create(vals)

    def write(self, vals):
        if 'room_id' not in vals and self.env.context.get('default_room_id'):
            vals['room_id'] = self.env.context['default_room_id']
        return super(HotelRoomAmenity, self).write(vals)