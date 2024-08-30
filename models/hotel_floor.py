from odoo import models, fields

class HotelFloor(models.Model):
    _name = 'hotel.floor'
    _description = 'Hotel Floor'

    name = fields.Char(string='Floor Name', required=True)
    manager_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Managers',
        help="Managers of the floor",
        widget='many2many_tags'
    )
