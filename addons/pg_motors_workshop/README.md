# P&G Motors Workshop Management System

## Overview

Complete workshop management solution for automotive repair shops built on Odoo 19.

## Features

### Customer & Vehicle Management
- Complete customer database with contact information
- Vehicle tracking with service history
- Automatic vehicle brand logo matching
- Import from legacy MySQL databases (1,869+ customers, 3,758+ vehicles)

### Workshop Operations
- Job cards and repair orders
- Labour time tracking with customizable rates
- Parts inventory management
- Sequential job numbering (WS00001, WS00002, etc.)
- Job status workflow (Draft → In Progress → Completed → Invoiced)
- Odometer tracking

### Invoice Generation
- Professional Australian tax invoice format
- Automatic GST (10%) calculations
- Labour and parts breakdown
- PDF generation with one click
- Email integration ready
- Customizable invoice template

### OCR Email Invoice Processing
- Automatic vendor invoice processing from emails
- PDF text extraction using PyPDF2
- Intelligent data parsing (vendor, amounts, dates)
- Automatic vendor matching
- Manual review workflow
- One-click bill creation

### Reporting
- Service history by vehicle
- Customer job tracking
- Mechanic performance
- Financial reports

## Installation

### Prerequisites

```bash
# Install PyPDF2 for OCR functionality
pip install PyPDF2
```

### Install Module

1. Copy `pg_motors_workshop` folder to your Odoo addons directory
2. Update your addons list:
```bash
python odoo-bin -c odoo.conf --addons-path=/path/to/addons -d your_database -u all
```

3. Go to Apps in Odoo interface
4. Search for "P&G Motors Workshop"
5. Click Install

## Initial Setup

### 1. Import Your Data

**Go to:** Workshop → Configuration → Import MySQL Data

1. Upload your MySQL dump file (`.sql`)
2. Select import options:
   - ✅ Import Customers
   - ✅ Import Vehicles
   - ✅ Auto-Match Vehicle Brands
3. Click "Import"

**Expected Results:**
- Customers with all contact details
- Vehicles linked to customers
- Automatic brand matching (CHEV → Chevrolet, etc.)
- Brand logos automatically assigned

### 2. Configure Vehicle Brands

**Go to:** Workshop → Configuration → Vehicle Brands

- Review pre-loaded brands (24 common brands included)
- Add custom brands as needed
- Upload brand logos
- Set abbreviations for auto-matching

### 3. Setup User Access

**Go to:** Settings → Users & Companies → Users

Assign groups:
- **Workshop User**: Create/edit jobs, view reports
- **Workshop Manager**: Full access including configuration

### 4. Configure Email for OCR (Optional)

**Go to:** Settings → Technical → Incoming Mail Servers

1. Setup email account for receiving vendor invoices
2. Configure fetchmail
3. Vendor invoice PDFs will be automatically processed

## Usage

### Creating a Workshop Job

1. **Go to:** Workshop → Operations → Workshop Jobs
2. Click "Create"
3. Fill in details:
   - Customer
   - Vehicle (auto-filtered by customer)
   - Job description
   - Odometer reading
4. Add Labour:
   - Description
   - Hours
   - Rate per hour
5. Add Parts:
   - Description/Product
   - Part number
   - Quantity
   - Unit price
6. Save

### Job Workflow

```
Draft → In Progress → Completed → Invoiced
           ↓
    Waiting for Parts
```

**Actions:**
- **Start Job**: Marks job as in progress
- **Complete Job**: Marks completed, updates vehicle odometer
- **Create Invoice**: Generates Odoo invoice from job
- **Print Invoice**: Downloads professional PDF invoice

### Generating Invoices

**From Job:**
1. Open completed job
2. Click "Print" → "Workshop Invoice"
3. PDF downloads automatically

**Features:**
- Professional Australian format
- Company branding (P&G Motors)
- Customer & vehicle details boxes
- Labour and parts tables
- GST calculation
- Payment terms
- Warranty information

### Processing Vendor Invoices (OCR)

**Automatic Processing:**
1. Send invoice PDF to configured email
2. System automatically:
   - Extracts text from PDF
   - Parses invoice data
   - Matches vendor
   - Creates OCR record
   - Notifies you for review

**Manual Review:**
1. **Go to:** Workshop → Invoicing → Vendor Invoice OCR
2. Review pending invoices
3. Verify extracted data:
   - Vendor
   - Invoice number
   - Amounts
   - Dates
4. Click "Approve"
5. Click "Create Bill"
6. Vendor bill created in Accounting

## Data Migration

### Supported MySQL Tables

**CLIENTS Table:**
```sql
CLIENT_ID, NAME, PHONE, MOBILE, EMAIL, STREET, CITY, STATE, ZIP
```

**VEHICLES Table:**
```sql
REGO, CLIENT_ID, MAKE, MODEL, YEAR, VIN, ENGINE_NO, COLOR
```

### Brand Abbreviation Matching

Pre-configured for common Australian abbreviations:
- CHEV, CHEVROLET → Chevrolet
- MERC, MERCEDES → Mercedes-Benz
- VOLKS, VW → Volkswagen
- And 20+ more brands

### Test Import First

Always test with a small dataset (5-10 records) before full import:

```sql
-- Create test file with first 5 records
SELECT * FROM CLIENTS LIMIT 5;
SELECT * FROM VEHICLES LIMIT 5;
```

## Customization

### Invoice Template

File: `reports/job_invoice_report.xml`

Customize:
- Colors (`#0066cc` → your brand color)
- Company name and details
- Logo (add to external_layout)
- Header/footer text
- Payment terms
- Warranty text

### Labour Rates

Default: $120/hour

Change in: `models/job_labour.py`
```python
rate = fields.Monetary(string='Rate per Hour', required=True, default=120.0)
```

### Job Number Prefix

Default: `WS00001`

Change in: `data/service_types_data.xml`
```xml
<field name="prefix">WS</field>  <!-- Change to your prefix -->
```

## Troubleshooting

### OCR Not Working

```bash
# Install PyPDF2
pip install PyPDF2

# Restart Odoo
sudo service odoo restart

# Update module
python odoo-bin -c odoo.conf -d your_database -u pg_motors_workshop --stop-after-init
```

### Import Fails

1. Check SQL file format (MySQL dump)
2. Verify table names match: `CLIENTS`, `VEHICLES`
3. Check column order in SQL
4. Review import log in wizard

### Brand Logos Not Showing

1. Go to: Configuration → Vehicle Brands
2. Edit brand
3. Upload logo image
4. Save
5. Re-assign brand to vehicles if needed

## Technical Details

### Dependencies

**Odoo Modules:**
- `base`
- `mail`
- `account`
- `stock`
- `fleet`
- `contacts`
- `product`
- `sale_management`
- `web`

**Python Libraries:**
- `PyPDF2` (for OCR)

### Database Schema

**Models Created:**
- `pg.motors.customer` - Customer records
- `pg.motors.vehicle` - Vehicle records
- `pg.motors.vehicle.brand` - Brand master data
- `pg.motors.workshop.job` - Workshop jobs
- `pg.motors.job.labour` - Labour lines
- `pg.motors.job.parts` - Parts lines
- `vendor.invoice.ocr` - OCR processing records

### Security Groups

- `group_pg_motors_user` - Workshop User
- `group_pg_motors_manager` - Workshop Manager

## Support

For issues or questions:
1. Check the documentation above
2. Review the deliverables summary
3. Check training guides included
4. Contact your system administrator

## Version History

**Version 19.0.1.0.0**
- Initial release
- Customer & vehicle management
- Workshop job cards
- Invoice generation with PDF
- OCR email invoice processing
- MySQL data import
- 24 pre-configured vehicle brands
- Complete documentation

## License

LGPL-3

## Credits

Developed for P&G Motors Workshop Management System
Built on Odoo 19.0
