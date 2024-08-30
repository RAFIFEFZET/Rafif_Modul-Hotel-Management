from odoo import models, fields

class HotelAmenity(models.Model):
    _name = 'hotel.amenity'
    _description = 'Hotel Amenity'

    name = fields.Char(string='Amenity Name', required=True)
    icon = fields.Binary(string='Icon')
    product_id = fields.Many2one('product.product', string='Related Product', readonly=True)
    list_price = fields.Float(string='List Price', help="The price of the amenity")

    def create(self, vals):
        res = super(HotelAmenity, self).create(vals)
        if res:
            product_vals = {
                'name': res.name,
                'type': 'service',
                'uom_id': self.env.ref('uom.product_uom_unit').id,
                'uom_po_id': self.env.ref('uom.product_uom_unit').id,
                'image_1920': res.icon,
                'list_price': res.list_price,
            }
            product = self.env['product.product'].create(product_vals)
            res.product_id = product.id
        return res
