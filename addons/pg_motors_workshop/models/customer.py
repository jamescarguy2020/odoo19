# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PGMotorsCustomer(models.Model):
    _name = 'pg.motors.customer'
    _description = 'P&G Motors Customer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Customer Name', required=True, tracking=True)
    customer_id = fields.Char(string='Customer ID', copy=False)
    partner_id = fields.Many2one('res.partner', string='Related Contact', ondelete='restrict')
    
    # Contact Information
    phone = fields.Char(string='Phone', tracking=True)
    mobile = fields.Char(string='Mobile', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    
    # Address
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='Postal Code')
    country_id = fields.Many2one('res.country', string='Country', default=lambda self: self.env.ref('base.au'))
    
    # Relationships
    vehicle_ids = fields.One2many('pg.motors.vehicle', 'customer_id', string='Vehicles')
    vehicle_count = fields.Integer(string='Vehicle Count', compute='_compute_vehicle_count')
    job_ids = fields.One2many('pg.motors.workshop.job', 'customer_id', string='Workshop Jobs')
    job_count = fields.Integer(string='Job Count', compute='_compute_job_count')
    
    # Additional Info
    notes = fields.Text(string='Notes')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('customer_id_unique', 'unique(customer_id)', 'Customer ID must be unique!')
    ]

    @api.depends('vehicle_ids')
    def _compute_vehicle_count(self):
        for customer in self:
            customer.vehicle_count = len(customer.vehicle_ids)

    @api.depends('job_ids')
    def _compute_job_count(self):
        for customer in self:
            customer.job_count = len(customer.job_ids)

    def action_view_vehicles(self):
        """View customer vehicles"""
        self.ensure_one()
        return {
            'name': 'Customer Vehicles',
            'type': 'ir.actions.act_window',
            'res_model': 'pg.motors.vehicle',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }

    def action_view_jobs(self):
        """View customer jobs"""
        self.ensure_one()
        return {
            'name': 'Customer Jobs',
            'type': 'ir.actions.act_window',
            'res_model': 'pg.motors.workshop.job',
            'view_mode': 'tree,form',
            'domain': [('customer_id', '=', self.id)],
            'context': {'default_customer_id': self.id},
        }
