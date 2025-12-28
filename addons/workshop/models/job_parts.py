# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JobParts(models.Model):
    _name = 'workshop.job.parts'
    _description = 'Workshop Job Parts'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    job_id = fields.Many2one('workshop.workshop.job', string='Job', required=True, ondelete='cascade')
    
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char(string='Description', required=True)
    part_number = fields.Char(string='Part Number')
    
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    unit_price = fields.Monetary(string='Unit Price', required=True)
    total = fields.Monetary(string='Total', compute='_compute_total', store=True)
    
    supplier_id = fields.Many2one('res.partner', string='Supplier', domain=[('supplier_rank', '>', 0)])
    notes = fields.Text(string='Notes')
    
    currency_id = fields.Many2one(related='job_id.currency_id', string='Currency', readonly=True)
    company_id = fields.Many2one(related='job_id.company_id', string='Company', readonly=True)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for part in self:
            part.total = part.quantity * part.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.part_number = self.product_id.default_code
            self.unit_price = self.product_id.list_price
