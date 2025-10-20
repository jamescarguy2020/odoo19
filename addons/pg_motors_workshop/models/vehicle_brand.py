# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VehicleBrand(models.Model):
    _name = 'pg.motors.vehicle.brand'
    _description = 'Vehicle Brand'
    _order = 'name'

    name = fields.Char(string='Brand Name', required=True)
    logo = fields.Binary(string='Brand Logo')
    logo_filename = fields.Char(string='Logo Filename')
    abbreviations = fields.Char(string='Common Abbreviations', help='Comma-separated abbreviations (e.g., CHEV,CHEVROLET)')
    active = fields.Boolean(default=True)
    vehicle_count = fields.Integer(string='Vehicle Count', compute='_compute_vehicle_count')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Brand name must be unique!')
    ]

    @api.depends('name')
    def _compute_vehicle_count(self):
        for brand in self:
            brand.vehicle_count = self.env['pg.motors.vehicle'].search_count([('brand_id', '=', brand.id)])

    @api.model
    def find_brand_by_abbreviation(self, abbr):
        """Find brand by abbreviation (e.g., 'CHEV' -> 'Chevrolet')"""
        if not abbr:
            return self.env['pg.motors.vehicle.brand']
        
        abbr_upper = abbr.upper().strip()
        
        # Direct name match first
        brand = self.search([('name', '=ilike', abbr)], limit=1)
        if brand:
            return brand
        
        # Search in abbreviations
        all_brands = self.search([])
        for brand in all_brands:
            if brand.abbreviations:
                abbrevs = [a.strip().upper() for a in brand.abbreviations.split(',')]
                if abbr_upper in abbrevs:
                    return brand
        
        return self.env['pg.motors.vehicle.brand']
