# 🧪 END-TO-END WORKSHOP TEST PROTOCOL

**Purpose:** Test the ACTUAL workflow from Job Card → Invoice → PDF → Email  
**Target User:** 14-year-old who just clicks buttons (needs to WORK)  
**Date:** October 24, 2025

---

## 🚨 CRITICAL ISSUE IDENTIFIED

**The workshop addon files exist, BUT Odoo is NOT running and dependencies are NOT installed.**

### Current State:
- ✅ Workshop addon files present at `/workspace/addons/workshop/`
- ❌ Odoo server is NOT running
- ❌ Python dependencies (babel, psycopg2, etc.) NOT installed
- ❌ Database likely NOT configured
- ❌ Cannot test workflow until environment is set up

---

## 📋 PRE-FLIGHT CHECKLIST (MUST DO FIRST)

### Step 1: Install Python Dependencies
```bash
cd /workspace
pip install -r requirements.txt

# OR install manually:
pip install babel
pip install psycopg2-binary
pip install PyPDF2
pip install Pillow
pip install lxml
pip install reportlab
pip install werkzeug
pip install gevent
# ... and all other Odoo requirements
```

### Step 2: Configure Database
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# If not installed, install it
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create Odoo database
sudo -u postgres createdb workshop_test

# Create Odoo user
sudo -u postgres createuser -s odoo
```

### Step 3: Create Odoo Configuration
```bash
# Create odoo.conf
cat > /workspace/odoo.conf << 'EOF'
[options]
addons_path = /workspace/addons
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = False
http_port = 8069
logfile = /workspace/odoo.log
log_level = info
EOF
```

### Step 4: Start Odoo Server
```bash
cd /workspace
python3 odoo-bin -c odoo.conf -d workshop_test --init=workshop
```

### Step 5: Access Odoo
```
URL: http://localhost:8069
Database: workshop_test
Email: admin
Password: admin (change on first login)
```

---

## 🎯 WORKFLOW TEST PLAN (After Setup)

### Test 1: Module Installation ✓

**Expected Result:**
- Workshop menu appears in main menu bar
- No errors in log file

**How to Verify:**
1. Open browser: `http://localhost:8069`
2. Login
3. Look for "Workshop" in top menu
4. Click Workshop → see menu items

---

### Test 2: Create Customer ✓

**Steps:**
1. Click **Workshop → Customers**
2. Click **New** button
3. Fill in:
   - Customer Name: "Test Customer"
   - Phone: "0412345678"
   - Mobile: "0412345678"
   - Email: "test@example.com"
4. Click **Save**

**Expected Result:**
- Customer saved with ID
- No errors
- Customer appears in list

**Screenshot:** (Take screenshot here)

---

### Test 3: Create Vehicle ✓

**Steps:**
1. Click **Workshop → Vehicles**
2. Click **New** button
3. Fill in:
   - Registration: "TEST123"
   - Owner: Select "Test Customer" (from dropdown)
   - Make: "Toyota"
   - Model: "Camry"
   - Year: "2020"
   - Odometer: "50000"
4. Click **Save**

**Expected Result:**
- Vehicle saved
- Owner linked correctly
- Brand logo appears (if configured)

**Screenshot:** (Take screenshot here)

---

### Test 4: Create Job Card (Booking Stage) ✓

**Steps:**
1. Click **Workshop → Job Cards**
2. Click **New** button
3. Fill in:
   - Customer: Select "Test Customer"
   - Vehicle: Select "TEST123"
   - Job Date: Today's date
   - Odometer Reading: "50000"
   - Description: "Test job - oil change and brake inspection"
4. Click **Save**

**Expected Result:**
- Job number generated (e.g., WS00001)
- Status = "Draft" or "Booking"
- All fields saved correctly

**CRITICAL CHECK:** 
- ❓ Does the job number appear?
- ❓ Is the workflow guidance visible at bottom?

**Screenshot:** (Take screenshot here)

---

### Test 5: Add Labour Lines ✓

**Steps:**
1. In the job card, scroll to **Labour** tab/section
2. Click **Add a line**
3. Fill in:
   - Description: "Oil change service"
   - Hours: "1.5"
   - Rate: "120.00" (should auto-fill)
   - Mechanic: (select if available)
4. Click **Add a line** again
5. Fill in:
   - Description: "Brake inspection and adjustment"
   - Hours: "0.5"
   - Rate: "120.00"
6. Click **Save**

**Expected Result:**
- Two labour lines visible
- Amounts calculated: 1.5 × 120 = $180, 0.5 × 120 = $60
- Labour total: $240

**CRITICAL CHECK:**
- ❓ Do the amounts calculate automatically?
- ❓ Does the labour total update?

**Screenshot:** (Take screenshot here)

---

### Test 6: Add Parts ✓

**Steps:**
1. Scroll to **Parts** tab/section
2. Click **Add a line**
3. Fill in:
   - Description: "Engine oil 5W-30"
   - Part Number: "OIL-5W30-5L"
   - Quantity: "5" (litres)
   - Unit Price: "12.00"
4. Click **Add a line** again
5. Fill in:
   - Description: "Oil filter"
   - Part Number: "FILTER-123"
   - Quantity: "1"
   - Unit Price: "25.00"
6. Click **Save**

**Expected Result:**
- Two parts lines visible
- Amounts calculated: 5 × 12 = $60, 1 × 25 = $25
- Parts total: $85

**CRITICAL CHECK:**
- ❓ Do the amounts calculate automatically?
- ❓ Does the parts total update?

**Screenshot:** (Take screenshot here)

---

### Test 7: Check Financial Calculations ✓

**Expected Result:**
- Labour Total: $240.00
- Parts Total: $85.00
- Subtotal: $325.00
- GST (10%): $32.50
- **Total: $357.50**

**CRITICAL CHECK:**
- ❓ Are all calculations correct?
- ❓ Is GST calculated at 10%?
- ❓ Is the total bold/highlighted?

**Screenshot:** (Take screenshot here)

---

### Test 8: Change Job State to "In Progress" ✓

**Steps:**
1. Look for state buttons at top of form (Draft, Scheduled, In Progress, etc.)
2. Click **"In Progress"** button or **"Start Work"** button
3. Confirm if prompted

**Expected Result:**
- Job state changes to "In Progress"
- Status indicator updates (color change?)
- Workflow guidance updates to show next steps

**CRITICAL CHECK:**
- ❓ Did the state change visibly?
- ❓ Did the workflow guidance update?
- ❓ Are the correct buttons now visible?

**Screenshot:** (Take screenshot here)

---

### Test 9: Complete the Job ✓

**Steps:**
1. Click **"Complete"** button or **"Mark Complete"**
2. Confirm if prompted

**Expected Result:**
- Job state changes to "Completed"
- Workflow guidance shows: "Next: Create invoice"

**CRITICAL CHECK:**
- ❓ Can you still edit labour/parts after completing?
- ❓ Is there a visible "Create Invoice" button?

**Screenshot:** (Take screenshot here)

---

### Test 10: Generate Invoice ✓

**Steps:**
1. Click **"Create Invoice"** button
2. Wait for invoice to be created
3. Check if redirected to invoice or if invoice reference appears

**Expected Result:**
- Invoice created and linked to job
- Invoice number visible (e.g., INV/2025/0001)
- Invoice total matches job total: $357.50
- All labour and parts transferred to invoice lines

**CRITICAL CHECK:**
- ❓ Was the invoice created?
- ❓ Does the invoice total match?
- ❓ Are labour and parts on separate lines?
- ❓ Is GST calculated correctly on the invoice?

**Screenshot:** (Take screenshot here)

---

### Test 11: Generate PDF Invoice ✓ **CRITICAL TEST**

**Steps:**
1. From the invoice screen, click **Print** button
2. Select **"Workshop Invoice"** or **"Job Invoice"** report
3. Wait for PDF to generate
4. PDF should download or open in new tab

**Expected Result:**
- PDF generates successfully
- PDF contains:
  - ✅ "TAX INVOICE" header
  - ✅ Job number (WS00001)
  - ✅ Customer details (name, phone, email)
  - ✅ Vehicle details (rego, make, model)
  - ✅ Labour table with hours and rates
  - ✅ Parts table with quantities and prices
  - ✅ Subtotal, GST, and Total
  - ✅ Payment terms
  - ✅ Professional formatting

**CRITICAL CHECK:**
- ❓ Did the PDF generate without errors?
- ❓ Does it look professional?
- ❓ Are all details correct?
- ❓ Is it ready to send to a customer?

**Screenshot:** (Save the PDF and take screenshot)

---

### Test 12: Email PDF to Customer ✓ **CRITICAL TEST**

**Steps:**
1. From invoice screen, click **"Send & Print"** button
2. Email composer should open with:
   - To: test@example.com
   - Subject: Invoice INV/2025/0001
   - PDF attached
3. Click **"Send Email"**

**Expected Result:**
- Email sent successfully
- Email appears in Sent Items or Chatter
- Customer receives email with PDF attachment

**CRITICAL CHECK:**
- ❓ Did the email send without errors?
- ❓ Is the PDF attached?
- ❓ Did the customer receive it? (Check test email)

**Known Issue:** User mentioned "Email system broken (OAuth/MSN/Automation Premium won't upgrade)"

**Alternative Test:**
1. Click **"Send & Print"**
2. Instead of sending, click **"Download"** to save PDF
3. Manually email PDF using Outlook/Gmail

**Screenshot:** (Take screenshot of email composer and sent confirmation)

---

## 🔴 FAILURE POINTS TO CHECK

### If Module Won't Install:
- Check `/workspace/odoo.log` for errors
- Verify all dependencies in `__manifest__.py` exist
- Check for Python syntax errors: `python3 -m py_compile addons/workshop/models/*.py`
- Verify security files are correct

### If Job Card Won't Save:
- Check database constraints
- Verify all required fields are filled
- Check for JavaScript errors in browser console (F12)
- Check Odoo log for ORM errors

### If Calculations Wrong:
- Check `workshop_job.py` compute methods
- Verify `job_labour.py` and `job_parts.py` calculations
- Check for currency/decimal field issues

### If PDF Won't Generate:
- Check `/workspace/addons/workshop/reports/job_invoice_report.xml`
- Verify QWeb template syntax
- Check for missing dependencies (reportlab, PyPDF2)
- Look for template rendering errors in log

### If Email Won't Send:
- Check Odoo email configuration: Settings → Technical → Email → Outgoing Mail Servers
- Verify SMTP settings
- Check for OAuth errors (known issue)
- Test with manual email as fallback

---

## 📊 SUCCESS CRITERIA

**The workflow is SUCCESSFUL if:**
- ✅ Job card number is generated (WS00001)
- ✅ Labour and parts are added without errors
- ✅ Financial calculations are correct
- ✅ Job state changes work (Draft → In Progress → Complete)
- ✅ Invoice is created from job
- ✅ **PDF generates with all correct information**
- ✅ **PDF can be emailed or downloaded for manual sending**

**If ANY of the above fail, the system is NOT ready for production.**

---

## 🎯 WHAT USER NEEDS

Based on the business context, the user needs:

### Immediate Requirements:
1. **Working job card → invoice → PDF workflow** (THIS TEST)
2. **Email delivery of invoices** (broken, needs fixing)
3. **No missed charges** (labour + parts + consumables)

### Future Requirements:
1. Automatic time tracking (not retrospective)
2. Parts auto-sourcing from eBay/supplier invoices
3. Quality checklist before completion
4. SMS notifications
5. Capacity dashboard (hours booked ahead)
6. Loaner vehicle tracking
7. Deferred work auto-copy

---

## 📝 TEST EXECUTION LOG

**Tester:** _____________  
**Date:** _____________  
**Odoo Version:** 19.0  
**Database:** workshop_test  

### Environment Setup:
- [ ] Python dependencies installed
- [ ] PostgreSQL running
- [ ] Database created
- [ ] Odoo server started
- [ ] Workshop module installed
- [ ] No errors in log file

### Workflow Tests:
- [ ] Test 1: Module visible
- [ ] Test 2: Customer created
- [ ] Test 3: Vehicle created
- [ ] Test 4: Job card created (number: ________)
- [ ] Test 5: Labour added (total: $________)
- [ ] Test 6: Parts added (total: $________)
- [ ] Test 7: Calculations correct (total: $________)
- [ ] Test 8: State changed to In Progress
- [ ] Test 9: Job completed
- [ ] Test 10: Invoice created (number: ________)
- [ ] Test 11: **PDF generated successfully** ✓ or ✗
- [ ] Test 12: **Email sent successfully** ✓ or ✗

### Issues Found:
1. __________________________________________
2. __________________________________________
3. __________________________________________

### Overall Result:
- [ ] ✅ **PASS** - Workflow works end-to-end
- [ ] ❌ **FAIL** - See issues above

---

## 🚀 NEXT STEPS AFTER TEST

### If Tests PASS:
1. Document the working workflow
2. Create user training guide
3. Import real customer/vehicle data
4. Train workshop staff
5. Go live with first real job

### If Tests FAIL:
1. Document each failure point
2. Fix issues one by one
3. Re-test after each fix
4. Don't move to next test until current one passes

---

**REMEMBER:** The user said it perfectly: "IF YOU WERE A 14 YEAR OLD THAT DID NOT KNOW WHAT TO DO BUT PRESS BUTTONS YES THE SCREEN CHANGE"

**This means:** It needs to ACTUALLY WORK when you click through it, not just have the files exist!

---

*This protocol must be executed by an agent with browser access to Odoo interface.*
