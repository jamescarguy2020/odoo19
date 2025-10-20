# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WorkshopJob(models.Model):
    _name = 'pg.motors.workshop.job'
    _description = 'Workshop Job Card'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'job_number desc, id desc'

    name = fields.Char(string='Job Description', required=True, tracking=True)
    job_number = fields.Char(string='Job Number', required=True, copy=False, readonly=True, default='New')
    
    # Customer & Vehicle
    customer_id = fields.Many2one('pg.motors.customer', string='Customer', required=True, tracking=True)
    vehicle_id = fields.Many2one('pg.motors.vehicle', string='Vehicle', required=True, tracking=True, domain="[('customer_id', '=', customer_id)]")
    registration = fields.Char(related='vehicle_id.registration_number', string='Registration', readonly=True)
    
    # Job Details
    job_date = fields.Date(string='Job Date', default=fields.Date.context_today, required=True, tracking=True)
    scheduled_date = fields.Datetime(string='Scheduled Date/Time')
    completion_date = fields.Datetime(string='Completion Date/Time')
    
    odometer_reading = fields.Float(string='Odometer Reading (km)')
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('waiting_parts', 'Waiting for Parts'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True)
    
    # Assigned To
    mechanic_id = fields.Many2one('res.users', string='Assigned Mechanic', tracking=True)
    
    # Service Lines
    labour_ids = fields.One2many('pg.motors.job.labour', 'job_id', string='Labour')
    parts_ids = fields.One2many('pg.motors.job.parts', 'job_id', string='Parts')
    
    # Costs & Pricing
    labour_total = fields.Monetary(string='Labour Total', compute='_compute_totals', store=True)
    parts_total = fields.Monetary(string='Parts Total', compute='_compute_totals', store=True)
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_totals', store=True)
    tax_amount = fields.Monetary(string='GST (10%)', compute='_compute_totals', store=True)
    total_amount = fields.Monetary(string='Total Amount', compute='_compute_totals', store=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    # Invoice
    invoice_id = fields.Many2one('account.move', string='Invoice', readonly=True, copy=False)
    invoice_status = fields.Selection([
        ('not_invoiced', 'Not Invoiced'),
        ('invoiced', 'Invoiced'),
    ], string='Invoice Status', compute='_compute_invoice_status', store=True)
    
    # Notes
    service_notes = fields.Text(string='Service Notes')
    internal_notes = fields.Text(string='Internal Notes')
    
    # Additional
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if vals.get('job_number', 'New') == 'New':
            vals['job_number'] = self.env['ir.sequence'].next_by_code('pg.motors.workshop.job') or 'New'
        return super(WorkshopJob, self).create(vals)

    @api.depends('labour_ids.total', 'parts_ids.total')
    def _compute_totals(self):
        for job in self:
            labour_total = sum(job.labour_ids.mapped('total'))
            parts_total = sum(job.parts_ids.mapped('total'))
            subtotal = labour_total + parts_total
            tax_amount = subtotal * 0.10  # 10% GST
            
            job.labour_total = labour_total
            job.parts_total = parts_total
            job.subtotal = subtotal
            job.tax_amount = tax_amount
            job.total_amount = subtotal + tax_amount

    @api.depends('invoice_id')
    def _compute_invoice_status(self):
        for job in self:
            job.invoice_status = 'invoiced' if job.invoice_id else 'not_invoiced'

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.customer_id = self.vehicle_id.customer_id
            if self.vehicle_id.odometer:
                self.odometer_reading = self.vehicle_id.odometer

    def action_start_job(self):
        """Mark job as in progress"""
        self.write({'state': 'in_progress'})

    def action_complete_job(self):
        """Mark job as completed"""
        self.write({
            'state': 'completed',
            'completion_date': fields.Datetime.now(),
        })
        # Update vehicle odometer
        if self.odometer_reading:
            self.vehicle_id.odometer = self.odometer_reading

    def action_create_invoice(self):
        """Create invoice from job"""
        self.ensure_one()
        
        if self.invoice_id:
            raise ValidationError(_('Invoice already exists for this job!'))
        
        invoice_lines = []
        
        # Add labour lines
        for labour in self.labour_ids:
            invoice_lines.append((0, 0, {
                'name': labour.description,
                'quantity': labour.hours,
                'price_unit': labour.rate,
                'tax_ids': [(6, 0, [self.env.ref('account.tax_sale_10').id])] if self.env.ref('account.tax_sale_10', False) else [],
            }))
        
        # Add parts lines
        for part in self.parts_ids:
            invoice_lines.append((0, 0, {
                'name': part.description,
                'product_id': part.product_id.id if part.product_id else False,
                'quantity': part.quantity,
                'price_unit': part.unit_price,
                'tax_ids': [(6, 0, [self.env.ref('account.tax_sale_10').id])] if self.env.ref('account.tax_sale_10', False) else [],
            }))
        
        # Create invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.partner_id.id if self.customer_id.partner_id else self.customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': invoice_lines,
            'narration': f"Workshop Job: {self.job_number}\nVehicle: {self.vehicle_id.name}",
        })
        
        self.write({
            'invoice_id': invoice.id,
            'state': 'invoiced',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_invoice(self):
        """View invoice"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
