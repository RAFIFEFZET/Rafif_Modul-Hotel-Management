from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomBookingLine(models.Model):
    _name = 'room.booking.line'
    _description = 'Room Booking Line'

    room_id = fields.Many2one('hotel.room', string='Room', required=True, ondelete='cascade')
    booking_id = fields.Many2one('room.booking', string='Booking Reference', ondelete='cascade')
    checkin_date = fields.Datetime(string='Check-In Date', required=True)
    checkout_date = fields.Datetime(string='Check-Out Date', required=True)
    uom_qty = fields.Float(string='Duration(Days)', readonly=True, compute='_compute_duration', store=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    price_unit = fields.Float(string='Unit Price', required=True)
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True)
    price_total = fields.Monetary(string='Total', compute='_compute_total', store=True)
    currency_id = fields.Many2one('res.currency', related='booking_id.currency_id', store=True)

    @api.depends('checkin_date', 'checkout_date')
    def _compute_duration(self):
        for line in self:
            if line.checkin_date and line.checkout_date:
                # Menghitung durasi dalam hari
                duration = (line.checkout_date - line.checkin_date).total_seconds() / 86400.0
                line.uom_qty = duration

    @api.depends('uom_qty', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.uom_qty

    @api.depends('price_subtotal')
    def _compute_total(self):
        for line in self:
            # Since tax is not used, total is the same as subtotal
            line.price_total = line.price_subtotal

    @api.constrains('checkin_date', 'checkout_date')
    def _check_dates(self):
        for line in self:
            if line.checkin_date >= line.checkout_date:
                raise ValidationError("Check-Out Date should be after Check-In Date.")
            # Update room status based on booking dates
            line.room_id._update_status(line.checkin_date, line.checkout_date)

    @api.onchange('room_id')
    def onchange_room_id(self):
        if self.room_id:
            self.price_unit = self.room_id.rent_price