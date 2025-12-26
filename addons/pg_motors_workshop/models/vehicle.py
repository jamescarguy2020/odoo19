# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PGMotorsVehicle(models.Model):
    _name = 'pg.motors.vehicle'
    _description = 'P&G Motors Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'registration_number'

    name = fields.Char(string='Vehicle Name', compute='_compute_name', store=True)
    registration_number = fields.Char(string='Registration Number', required=True, tracking=True)
    vin = fields.Char(string='VIN Number', tracking=True)
    
    # Owner
    customer_id = fields.Many2one('pg.motors.customer', string='Owner', required=True, tracking=True, ondelete='restrict')
    customer_name = fields.Char(related='customer_id.name', string='Owner Name', readonly=True)
    customer_phone = fields.Char(related='customer_id.phone', string='Owner Phone', readonly=True)
    
    # Vehicle Details
    brand_id = fields.Many2one('pg.motors.vehicle.brand', string='Brand', tracking=True)
    brand_name = fields.Char(string='Brand Name (Text)', help='For imported data')
    model = fields.Char(string='Model', tracking=True)
    year = fields.Char(string='Year')
    color = fields.Char(string='Color')
    engine_number = fields.Char(string='Engine Number')
    transmission = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
    ], string='Transmission')
    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('lpg', 'LPG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], string='Fuel Type')
    
    # Odometer
    odometer = fields.Float(string='Current Odometer (km)')
    odometer_unit = fields.Selection([
        ('kilometers', 'Kilometers'),
        ('miles', 'Miles'),
    ], default='kilometers', string='Odometer Unit')
    
    # Relationships
    job_ids = fields.One2many('pg.motors.workshop.job', 'vehicle_id', string='Service Jobs')
    job_count = fields.Integer(string='Job Count', compute='_compute_job_count')
    
    # Additional Info
    notes = fields.Text(string='Notes')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    # Brand Logo (computed from brand)
    brand_logo = fields.Binary(related='brand_id.logo', string='Brand Logo', readonly=True)

    _sql_constraints = [
        ('registration_unique', 'unique(registration_number)', 'Registration number must be unique!')
    ]

    @api.depends('registration_number', 'brand_id', 'model')
    def _compute_name(self):
        for vehicle in self:
            parts = []
            if vehicle.registration_number:
                parts.append(vehicle.registration_number)
            if vehicle.brand_id:
                parts.append(vehicle.brand_id.name)
            elif vehicle.brand_name:
                parts.append(vehicle.brand_name)
            if vehicle.model:
                parts.append(vehicle.model)
            vehicle.name = ' - '.join(parts) if parts else 'New Vehicle'

    @api.depends('job_ids')
    def _compute_job_count(self):
        for vehicle in self:
            vehicle.job_count = len(vehicle.job_ids)

    @api.onchange('brand_name')
    def _onchange_brand_name(self):
        """Auto-match brand when brand_name changes"""
        if self.brand_name and not self.brand_id:
            brand = self.env['pg.motors.vehicle.brand'].find_brand_by_abbreviation(self.brand_name)
            if brand:
                self.brand_id = brand.id

    def action_view_jobs(self):
        """View vehicle service jobs"""
        self.ensure_one()
        return {
            'name': 'Vehicle Service Jobs',
            'type': 'ir.actions.act_window',
            'res_model': 'pg.motors.workshop.job',
            'view_mode': 'tree,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id, 'default_customer_id': self.customer_id.id},
        }
