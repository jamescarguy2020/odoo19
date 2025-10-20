# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JobLabour(models.Model):
    _name = 'pg.motors.job.labour'
    _description = 'Workshop Job Labour'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    job_id = fields.Many2one('pg.motors.workshop.job', string='Job', required=True, ondelete='cascade')
    
    description = fields.Char(string='Description', required=True)
    hours = fields.Float(string='Hours', default=1.0, required=True)
    rate = fields.Monetary(string='Rate per Hour', required=True, default=120.0)
    total = fields.Monetary(string='Total', compute='_compute_total', store=True)
    
    mechanic_id = fields.Many2one('res.users', string='Mechanic')
    notes = fields.Text(string='Notes')
    
    currency_id = fields.Many2one(related='job_id.currency_id', string='Currency', readonly=True)
    company_id = fields.Many2one(related='job_id.company_id', string='Company', readonly=True)

    @api.depends('hours', 'rate')
    def _compute_total(self):
        for labour in self:
            labour.total = labour.hours * labour.rate
