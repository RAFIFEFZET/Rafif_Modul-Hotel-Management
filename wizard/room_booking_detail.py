from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import json
import io
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class RoomBookingWizard(models.TransientModel):
    _name = "room.booking.detail"
    _description = "Room Booking Details"

    checkin = fields.Date(help="Choose the Checkin Date", string="Checkin")
    checkout = fields.Date(help="Choose the Checkout Date", string="Checkout")
    room_id = fields.Many2one("hotel.room", string="Room", help="Choose The Room")

    def action_room_booking_pdf(self):
        data = {
            "booking": self.generate_data(),
        }
        return self.env.ref("hotel_management.action_report_room_booking").report_action(self, data=data)


    def generate_data(self):
        domain = []
        if self.checkin and self.checkout:
            if self.checkin > self.checkout:
                raise ValidationError(_("Check-in date should be less than Check-out date"))
        if self.checkin:
            domain.append(("room_line_ids.checkin_date", ">=", self.checkin))
        if self.checkout:
            domain.append(("room_line_ids.checkout_date", "<=", self.checkout))
        if self.room_id:
            domain.append(("room_line_ids.room_id", "=", self.room_id.id))

        room_booking = self.env["room.booking"].search(domain)
        room_list = []
        for booking in room_booking:
            for line in booking.room_line_ids:
                room_list.append({
                    'partner_id': booking.partner_id.name,
                    'room_id': line.room_id.name,
                    'checkin_date': line.checkin_date,
                    'checkout_date': line.checkout_date,
                    'name': booking.name,
                })
        return room_list