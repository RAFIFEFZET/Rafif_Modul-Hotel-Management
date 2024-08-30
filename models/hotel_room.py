from odoo import api, fields, models

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string="Room Name", required=True)
    icon = fields.Binary(string='Icon')
    floor_id = fields.Many2one('hotel.floor', string="Floor")
    room_type = fields.Selection([('single', 'Single'), ('double', 'Double')], string="Room Type")
    rent_price = fields.Float(string="Rent Price")
    number_of_person = fields.Integer(string="Number of Person")
    description = fields.Html(string="Description")
    amenity_ids = fields.One2many('hotel.room.amenity', 'room_id', string='Amenities')
    total_amenity_cost = fields.Float(string="Total Amenity Cost", compute='_compute_total_amenity_cost', store=True)
    manager_id = fields.Many2one('res.users', string="Manager")
    status = fields.Selection([
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('occupied', 'Occupied'),
    ], string='Status', default='available')

    @api.depends('amenity_ids.total_price')
    def _compute_total_amenity_cost(self):
        for room in self:
            total_cost = sum(amenity.total_price for amenity in room.amenity_ids)
            room.total_amenity_cost = total_cost

    def _update_status(self, checkin_date, checkout_date):
        current_time = fields.Datetime.now()
        if checkin_date <= current_time < checkout_date:
            self.status = 'occupied'
        elif current_time >= checkout_date:
            self.status = 'available'
        else:
            self.status = 'booked'        
