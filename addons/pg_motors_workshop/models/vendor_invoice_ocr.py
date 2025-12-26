# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import logging

_logger = logging.getLogger(__name__)

try:
    import PyPDF2
    from io import BytesIO
except ImportError:
    _logger.warning("PyPDF2 not installed. OCR features will not work.")
    PyPDF2 = None


class VendorInvoiceOCR(models.Model):
    _name = 'vendor.invoice.ocr'
    _description = 'Vendor Invoice OCR Processing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Invoice Reference', required=True, tracking=True)
    state = fields.Selection([
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='pending', required=True, tracking=True)
    
    # Source
    email_from = fields.Char(string='Email From')
    email_subject = fields.Char(string='Email Subject')
    email_date = fields.Datetime(string='Email Date')
    
    # PDF Attachment
    pdf_file = fields.Binary(string='PDF Invoice', required=True, attachment=True)
    pdf_filename = fields.Char(string='Filename')
    
    # Extracted Data
    extracted_text = fields.Text(string='Extracted Text', readonly=True)
    
    # Invoice Details
    vendor_id = fields.Many2one('res.partner', string='Vendor', domain=[('supplier_rank', '>', 0)])
    vendor_name_extracted = fields.Char(string='Vendor Name (Extracted)', readonly=True)
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    due_date = fields.Date(string='Due Date')
    
    # Amounts
    subtotal = fields.Monetary(string='Subtotal', currency_field='currency_id')
    tax_amount = fields.Monetary(string='Tax Amount', currency_field='currency_id')
    total_amount = fields.Monetary(string='Total Amount', currency_field='currency_id')
    
    # Line Items
    line_items_text = fields.Text(string='Line Items (Extracted)', readonly=True)
    
    # Created Invoice
    bill_id = fields.Many2one('account.move', string='Vendor Bill', readonly=True, copy=False)
    
    # Additional
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    def action_extract_data(self):
        """Extract data from PDF using OCR"""
        self.ensure_one()
        
        if not PyPDF2:
            raise ValidationError(_('PyPDF2 library is not installed. Please install it using: pip install PyPDF2'))
        
        if not self.pdf_file:
            raise ValidationError(_('No PDF file attached!'))
        
        try:
            # Decode PDF
            pdf_data = base64.b64decode(self.pdf_file)
            pdf_file = BytesIO(pdf_data)
            
            # Extract text
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text() + '\n'
            
            self.extracted_text = text
            
            # Parse invoice data
            self._parse_invoice_data(text)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Success'),
                    'message': _('Data extracted successfully! Please review and approve.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"OCR extraction failed: {str(e)}")
            raise ValidationError(_('Failed to extract data from PDF: %s') % str(e))

    def _parse_invoice_data(self, text):
        """Parse invoice data from extracted text"""
        lines = text.split('\n')
        
        # Basic parsing logic (customize based on your vendor invoice formats)
        for i, line in enumerate(lines):
            line_upper = line.upper()
            
            # Try to extract invoice number
            if 'INVOICE' in line_upper and not self.invoice_number:
                # Look for patterns like "INVOICE #12345" or "INVOICE NO: 12345"
                import re
                match = re.search(r'INVOICE\s*(?:NO|#|NUMBER)?[\s:]*([A-Z0-9-]+)', line_upper)
                if match:
                    self.invoice_number = match.group(1)
            
            # Try to extract total
            if 'TOTAL' in line_upper and not self.total_amount:
                # Look for currency amounts
                import re
                match = re.search(r'\$?\s*([0-9,]+\.?\d{0,2})', line)
                if match:
                    try:
                        amount = float(match.group(1).replace(',', ''))
                        self.total_amount = amount
                    except:
                        pass
            
            # Try to extract vendor name (usually at top)
            if i < 5 and len(line.strip()) > 3 and not self.vendor_name_extracted:
                if not any(x in line_upper for x in ['INVOICE', 'TAX', 'ABN', 'ACN']):
                    self.vendor_name_extracted = line.strip()
        
        # Auto-match vendor
        if self.vendor_name_extracted and not self.vendor_id:
            vendor = self.env['res.partner'].search([
                ('name', 'ilike', self.vendor_name_extracted),
                ('supplier_rank', '>', 0)
            ], limit=1)
            if vendor:
                self.vendor_id = vendor.id

    def action_approve(self):
        """Approve OCR data"""
        self.write({'state': 'approved'})

    def action_create_bill(self):
        """Create vendor bill from OCR data"""
        self.ensure_one()
        
        if not self.vendor_id:
            raise ValidationError(_('Please select a vendor before creating a bill!'))
        
        if self.bill_id:
            raise ValidationError(_('Bill already created for this invoice!'))
        
        # Create vendor bill
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.vendor_id.id,
            'invoice_date': self.invoice_date or fields.Date.today(),
            'invoice_date_due': self.due_date,
            'ref': self.invoice_number or self.name,
            'narration': f"Created from OCR processing\nExtracted from: {self.pdf_filename}\n\n{self.notes or ''}",
        })
        
        self.write({
            'bill_id': bill.id,
            'state': 'processed',
        })
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': bill.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_reject(self):
        """Reject OCR processing"""
        self.write({'state': 'rejected'})

    def action_view_bill(self):
        """View created bill"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': self.bill_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
