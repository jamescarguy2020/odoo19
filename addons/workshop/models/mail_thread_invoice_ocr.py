# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.model
    def message_process(self, model, message_dict, save_original=False, strip_attachments=False, thread_id=None):
        """Override to process vendor invoices from emails"""
        result = super(MailThread, self).message_process(
            model, message_dict, save_original, strip_attachments, thread_id
        )
        
        # Check if email has PDF attachments (vendor invoices)
        if message_dict.get('attachments'):
            self._process_vendor_invoice_attachments(message_dict)
        
        return result

    def _process_vendor_invoice_attachments(self, message_dict):
        """Process PDF attachments as potential vendor invoices"""
        try:
            attachments = message_dict.get('attachments', [])
            email_from = message_dict.get('from', '')
            email_subject = message_dict.get('subject', '')
            email_date = message_dict.get('date')
            
            for attachment in attachments:
                filename = attachment[0] if attachment else ''
                file_data = attachment[1] if len(attachment) > 1 else None
                
                # Check if it's a PDF
                if filename and filename.lower().endswith('.pdf') and file_data:
                    # Check if subject/body indicates it's an invoice
                    is_invoice = any(keyword in email_subject.lower() for keyword in [
                        'invoice', 'bill', 'statement', 'tax invoice'
                    ])
                    
                    if is_invoice:
                        # Create OCR record
                        ocr_record = self.env['vendor.invoice.ocr'].sudo().create({
                            'name': f"Invoice from {email_from}",
                            'pdf_file': file_data,
                            'pdf_filename': filename,
                            'email_from': email_from,
                            'email_subject': email_subject,
                            'email_date': email_date,
                            'state': 'pending',
                        })
                        
                        # Auto-extract data
                        try:
                            ocr_record.action_extract_data()
                            _logger.info(f"Created OCR record {ocr_record.id} from email: {email_subject}")
                        except Exception as e:
                            _logger.error(f"Failed to auto-extract OCR data: {str(e)}")
                        
                        # Create activity for review
                        ocr_record.activity_schedule(
                            'mail.mail_activity_data_todo',
                            summary='Review Vendor Invoice',
                            note=f'New vendor invoice received via email from {email_from}. Please review and approve.',
                            user_id=self.env.ref('base.user_admin').id,
                        )
                        
        except Exception as e:
            _logger.error(f"Error processing vendor invoice attachments: {str(e)}")
