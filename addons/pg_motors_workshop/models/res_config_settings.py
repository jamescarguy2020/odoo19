# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Labour Rate Settings
    default_labour_rate = fields.Monetary(
        string='Default Labour Rate (per hour)',
        default=120.0,
        config_parameter='pg_motors_workshop.default_labour_rate',
        currency_field='currency_id',
        help='Default hourly rate for workshop labour'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
