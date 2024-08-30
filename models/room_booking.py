from odoo import models, fields, api, _

class RoomBooking(models.Model):
    _name = 'room.booking'
    _description = 'Room Booking'
    _order = 'name desc'

    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: self._get_default_name())
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True)
    date_order = fields.Datetime(string='Order Date', required=True, index=True, copy=False, default=fields.Datetime.now)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('check_in', 'Checked In'),
        ('check_out', 'Checked Out'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft')

    is_checkin = fields.Boolean(string='Is Check-In', readonly=True, copy=False, default=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    checkin_date = fields.Datetime(string='Check-In Date', readonly=True, copy=False)
    checkout_date = fields.Datetime(string='Check-Out Date', readonly=True, copy=False)
    duration = fields.Float(string='Duration', readonly=True)
    duration_visible = fields.Boolean(string='Duration Visible', default=True)
    room_line_ids = fields.One2many('room.booking.line', 'booking_id', string='Room Lines')
    amount_total = fields.Monetary(string='Total', readonly=True, store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    room_line_ids = fields.One2many('room.booking.line', 'booking_id', string='Room Lines')

    def action_reserve(self):
        self.write({'state': 'reserved'})
        for line in self.room_line_ids:
            line.room_id.write({'status': 'booked'})

    def action_checkin(self):
        self.write({'state': 'check_in', 'is_checkin': True})
        for line in self.room_line_ids:
            line.room_id.write({'status': 'occupied'})

    def action_checkout(self):
        self.write({'state': 'check_out'})
        for line in self.room_line_ids:
            line.room_id.write({'status': 'available'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
        for line in self.room_line_ids:
            line.room_id.write({'status': 'available'})

    def action_done(self):
        self.write({'state': 'done'})
        for line in self.room_line_ids:
            line.room_id.write({'status': 'available'})

    @api.depends('room_line_ids.price_subtotal')
    def _compute_amount_total(self):
        for booking in self:
            amount_untaxed = sum(line.price_subtotal for line in booking.room_line_ids)
            booking.update({
                'amount_total': amount_untaxed,
            })

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('room.booking.sequence') or 'New'
        return super(RoomBooking, self).create(vals)

    @api.model
    def _get_default_name(self):
        return self.env['ir.sequence'].next_by_code('room.booking.sequence') or 'New'