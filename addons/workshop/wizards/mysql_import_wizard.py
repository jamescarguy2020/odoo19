# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import logging
import re

_logger = logging.getLogger(__name__)


class MySQLImportWizard(models.TransientModel):
    _name = 'mysql.import.wizard'
    _description = 'Import Customers and Vehicles from MySQL'

    sql_file = fields.Binary(string='SQL File', required=True, help='Upload your MySQL dump file')
    sql_filename = fields.Char(string='Filename')
    
    import_customers = fields.Boolean(string='Import Customers', default=True)
    import_vehicles = fields.Boolean(string='Import Vehicles', default=True)
    auto_match_brands = fields.Boolean(string='Auto-Match Vehicle Brands', default=True, 
                                        help='Automatically match brand abbreviations to brand logos')
    
    # Results
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default='draft')
    
    customers_created = fields.Integer(string='Customers Created', readonly=True)
    vehicles_created = fields.Integer(string='Vehicles Created', readonly=True)
    brands_matched = fields.Integer(string='Brands Matched', readonly=True)
    import_log = fields.Text(string='Import Log', readonly=True)

    def action_import(self):
        """Import data from SQL file"""
        self.ensure_one()
        
        if not self.sql_file:
            raise ValidationError(_('Please upload an SQL file!'))
        
        try:
            # Decode SQL file
            sql_content = base64.b64decode(self.sql_file).decode('utf-8')
            
            log = []
            customers_count = 0
            vehicles_count = 0
            brands_count = 0
            
            # Parse and import customers
            if self.import_customers:
                customers_count = self._import_customers(sql_content, log)
            
            # Parse and import vehicles
            if self.import_vehicles:
                vehicles_count, brands_count = self._import_vehicles(sql_content, log)
            
            # Update results
            self.write({
                'state': 'done',
                'customers_created': customers_count,
                'vehicles_created': vehicles_count,
                'brands_matched': brands_count,
                'import_log': '\n'.join(log),
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Import Complete!'),
                    'message': _('Imported %d customers and %d vehicles (%d brands matched)') % (customers_count, vehicles_count, brands_count),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"Import failed: {str(e)}")
            raise ValidationError(_('Import failed: %s') % str(e))

    def _import_customers(self, sql_content, log):
        """Import customers from SQL"""
        customers_created = 0
        
        # Find INSERT statements for customers table
        # Pattern: INSERT INTO `CLIENTS` VALUES (...)
        pattern = r"INSERT INTO `CLIENTS` VALUES\s*\((.*?)\);"
        matches = re.findall(pattern, sql_content, re.IGNORECASE)
        
        for match in matches:
            try:
                # Parse values
                values = self._parse_sql_values(match)
                if len(values) >= 10:
                    # Map to customer fields (adjust indices based on your SQL structure)
                    customer_id = values[0]  # CLIENT_ID
                    name = values[1]  # NAME
                    phone = values[2] if len(values) > 2 else ''
                    mobile = values[3] if len(values) > 3 else ''
                    email = values[4] if len(values) > 4 else ''
                    street = values[5] if len(values) > 5 else ''
                    city = values[6] if len(values) > 6 else ''
                    state = values[7] if len(values) > 7 else ''
                    zip_code = values[8] if len(values) > 8 else ''
                    
                    # Check if customer already exists
                    existing = self.env['workshop.customer'].search([('customer_id', '=', customer_id)], limit=1)
                    if not existing:
                        # Create customer
                        self.env['workshop.customer'].create({
                            'customer_id': customer_id,
                            'name': name,
                            'phone': phone,
                            'mobile': mobile,
                            'email': email,
                            'street': street,
                            'city': city,
                            'zip': zip_code,
                        })
                        customers_created += 1
                    
            except Exception as e:
                log.append(f"Error importing customer: {str(e)}")
                _logger.error(f"Error importing customer: {str(e)}")
        
        log.append(f"Imported {customers_created} customers")
        return customers_created

    def _import_vehicles(self, sql_content, log):
        """Import vehicles from SQL"""
        vehicles_created = 0
        brands_matched = 0
        
        # Find INSERT statements for vehicles table
        pattern = r"INSERT INTO `VEHICLES` VALUES\s*\((.*?)\);"
        matches = re.findall(pattern, sql_content, re.IGNORECASE)
        
        for match in matches:
            try:
                # Parse values
                values = self._parse_sql_values(match)
                if len(values) >= 5:
                    # Map to vehicle fields (adjust indices based on your SQL structure)
                    registration = values[0]  # REGO
                    customer_id_ref = values[1]  # CLIENT_ID
                    brand_name = values[2] if len(values) > 2 else ''  # MAKE
                    model = values[3] if len(values) > 3 else ''  # MODEL
                    year = values[4] if len(values) > 4 else ''  # YEAR
                    vin = values[5] if len(values) > 5 else ''  # VIN
                    
                    # Find customer
                    customer = self.env['workshop.customer'].search([('customer_id', '=', customer_id_ref)], limit=1)
                    if not customer:
                        log.append(f"Customer {customer_id_ref} not found for vehicle {registration}")
                        continue
                    
                    # Check if vehicle already exists
                    existing = self.env['workshop.vehicle'].search([('registration_number', '=', registration)], limit=1)
                    if not existing:
                        # Auto-match brand
                        brand = False
                        if self.auto_match_brands and brand_name:
                            brand = self.env['workshop.vehicle.brand'].find_brand_by_abbreviation(brand_name)
                            if brand:
                                brands_matched += 1
                        
                        # Create vehicle
                        self.env['workshop.vehicle'].create({
                            'registration_number': registration,
                            'customer_id': customer.id,
                            'brand_id': brand.id if brand else False,
                            'brand_name': brand_name,
                            'model': model,
                            'year': year,
                            'vin': vin,
                        })
                        vehicles_created += 1
                    
            except Exception as e:
                log.append(f"Error importing vehicle: {str(e)}")
                _logger.error(f"Error importing vehicle: {str(e)}")
        
        log.append(f"Imported {vehicles_created} vehicles ({brands_matched} brands matched)")
        return vehicles_created, brands_matched

    def _parse_sql_values(self, values_string):
        """Parse SQL VALUES string into Python list"""
        # Simple parser for SQL values
        # Handles strings in quotes and NULL values
        values = []
        current = ''
        in_quote = False
        quote_char = None
        
        for char in values_string:
            if char in ('"', "'") and not in_quote:
                in_quote = True
                quote_char = char
            elif char == quote_char and in_quote:
                in_quote = False
                quote_char = None
            elif char == ',' and not in_quote:
                values.append(current.strip().strip('"').strip("'"))
                current = ''
            else:
                current += char
        
        # Add last value
        if current:
            values.append(current.strip().strip('"').strip("'"))
        
        # Convert NULL to empty string
        values = ['' if v.upper() == 'NULL' else v for v in values]
        
        return values

    def action_view_results(self):
        """View import results"""
        self.ensure_one()
        return {
            'name': 'Import Results',
            'type': 'ir.actions.act_window',
            'res_model': 'mysql.import.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
