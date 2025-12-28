# -*- coding: utf-8 -*-
{
    'name': 'Workshop Management',
    'version': '19.0.1.0.0',
    'category': 'Services/Automotive',
    'summary': 'Complete workshop management system for automotive repair shops',
    'description': """
Workshop Management System
==========================

Complete workshop management solution including:
* Customer and vehicle management
* Workshop job cards and repair orders
* Labour and parts tracking
* Invoice generation with PDF output
* OCR email invoice processing for vendor bills
* MySQL data import from legacy systems
* Automatic vehicle brand logo matching
* Comprehensive reporting
* Mechanic workflow training materials

Key Features:
-------------
* Import customers and vehicles from MySQL databases
* Professional invoice PDF generation
* OCR processing of vendor invoices via email
* Vehicle service history tracking
* Parts inventory management
* Labour time tracking
* Automated GST calculations
* Email integration for invoices
* Workflow documentation for training
    """,
    'author': 'Workshop',
    'website': 'https://www.workshop.local',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'account',
        'stock',
        'fleet',
        'contacts',
        'product',
        'sale_management',
        'web',
    ],
    'external_dependencies': {
        'python': ['PyPDF2'],
    },
    'data': [
        # Security
        'security/workshop_security.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/vehicle_brands_data.xml',
        'data/service_types_data.xml',
        
        # Views
        'views/menu_views.xml',
        'views/res_config_settings_views.xml',
        'views/customer_views.xml',
        'views/vehicle_views.xml',
        'views/workshop_job_views.xml',
        'views/job_labour_views.xml',
        'views/job_parts_views.xml',
        'views/vendor_invoice_ocr_views.xml',
        
        # Wizards
        'wizards/mysql_import_wizard_views.xml',
        
        # Reports
        'reports/job_invoice_report.xml',
        'reports/workshop_reports.xml',
    ],
    'assets': {
        # No custom assets - using standard Odoo theme
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
