# 🚨 CRITICAL: BROWSER TEST PLAN FOR WORKSHOP ADDON

**Date:** October 24, 2025  
**Purpose:** Test all 8 workflows in Chrome browser  
**Critical Issue:** Two different workshop installations detected!

---

## ⚠️ **CRITICAL ISSUE DETECTED**

### Two Different Workshop Installations Found:

**Installation 1: `/workspace/addons/workshop/`**
- Model: `workshop.workshop.job`
- Verified: October 24, 2025
- Status: ✅ All files verified, zero errors
- Views: Basic workshop_job_views.xml

**Installation 2: `Odoo19g/addons/workshop/`** (Location Unknown)
- Model: `workshop.job` (DIFFERENT!)
- File provided: `workshop_comprehensive_booking_views.xml`
- Has: Comprehensive 11-tab booking form
- Features: Timeline, work sessions, API lookup, service schedules

**⚠️ THESE ARE INCOMPATIBLE!**
- Different model names will cause errors
- Views reference different models
- Cannot mix files from both installations

---

## 🔍 **FIRST STEP: IDENTIFY ACTIVE INSTALLATION**

**Browser testing agent MUST:**

1. Open Odoo in Chrome
2. Navigate to Workshop menu
3. Open a job card
4. Check the browser URL:
   - If it says `/workshop.workshop.job/` → Using Installation 1
   - If it says `/workshop.job/` → Using Installation 2
5. Report back which installation is active

---

## 📋 **8 WORKFLOWS TO TEST**

Based on the comprehensive booking view, here are the 8 workflows:

### **Workflow 1: BOOKING → Create New Job**
**Path:** Booking stage (initial job creation)

**Test Steps:**
1. Click "Workshop" → "Job Cards" → "New"
2. Fill in customer (select from dropdown)
3. Fill in vehicle (select from dropdown)
4. Set scheduled drop-off date/time
5. Set scheduled pickup date/time
6. Set estimated hours
7. Assign technician
8. Click "Save"
9. Verify job number generated (e.g., WS00001)
10. Verify state = "Booking"

**Expected Behavior:**
- ✅ Job number auto-generates
- ✅ Customer/vehicle dropdowns populated
- ✅ All fields save correctly
- ✅ State badge shows "Booking"

**Failure Points:**
- ❌ Job number doesn't generate
- ❌ Customer/vehicle dropdowns empty
- ❌ Validation errors on save
- ❌ State doesn't update

**Strengths:**
- Simple, straightforward process
- Auto-numbered jobs
- Required fields validation

**Weaknesses:**
- No vehicle API lookup at this stage
- Manual customer/vehicle selection

---

### **Workflow 2: VEHICLE DETAILS → API Lookup**
**Path:** Vehicle Details tab

**Test Steps:**
1. Open existing job (created in Workflow 1)
2. Click "Vehicle Details" tab
3. Enter registration number in "temp_rego"
4. Select state in "temp_jurisdiction"
5. Click "RapidAPI Rego Lookup" button
6. Wait for API response
7. Check "lookup_status" field
8. Check "lookup_message" field
9. Verify vehicle details populated

**Expected Behavior:**
- ✅ API call completes
- ✅ Vehicle details auto-populate
- ✅ Status shows "Success" or error message
- ✅ Make, model, year, VIN filled

**Failure Points:**
- ❌ API key not configured
- ❌ API returns error
- ❌ Vehicle not found
- ❌ Fields don't populate

**Strengths:**
- Automated vehicle data entry
- Reduces manual typing errors

**Weaknesses:**
- Depends on external API
- API costs per lookup
- Australian rego only?

---

### **Workflow 3: LABOUR → Add Labour Lines**
**Path:** Labour tab

**Test Steps:**
1. Click "Labour" tab
2. Click "Add a line"
3. Enter description (e.g., "Full service - Oil, filters")
4. Enter hours (e.g., 2.5)
5. Verify rate auto-fills (default $120/hr)
6. Select technician
7. Verify subtotal calculates (Hours × Rate)
8. Add second labour line
9. Verify "Labour Total" at bottom updates
10. Save job

**Expected Behavior:**
- ✅ Inline editing works
- ✅ Rate defaults from settings
- ✅ Subtotal auto-calculates
- ✅ Labour total sums all lines
- ✅ Currency displays correctly

**Failure Points:**
- ❌ Rate doesn't default
- ❌ Calculation doesn't work
- ❌ Labour total doesn't update
- ❌ Decimal places wrong

**Strengths:**
- Inline editable list
- Auto-calculations
- Per-technician tracking

**Weaknesses:**
- Retrospective time entry (not live timer)
- No integration with work sessions

---

### **Workflow 4: PARTS → Add Parts with Markup**
**Path:** Parts tab

**Test Steps:**
1. Click "Parts" tab
2. Click "Add a line"
3. Enter description (e.g., "Engine Oil 5W-30")
4. Enter part number
5. Enter cost price (e.g., $15.00)
6. Enter markup percent (e.g., 30)
7. Verify selling price calculates (Cost × 1.30)
8. Enter quantity (e.g., 5)
9. Verify subtotal calculates (Qty × Selling Price)
10. Add supplier
11. Mark "is_supplied" if customer-supplied part
12. Verify "Parts Total" updates
13. Save job

**Expected Behavior:**
- ✅ Selling price = Cost × (1 + Markup%)
- ✅ Subtotal = Qty × Selling Price
- ✅ Parts total sums all lines
- ✅ Supplier dropdown works
- ✅ Customer-supplied flag works

**Failure Points:**
- ❌ Markup calculation wrong
- ❌ Decimal rounding errors
- ❌ Parts total doesn't update
- ❌ Supplier dropdown empty

**Strengths:**
- Built-in markup calculator
- Customer-supplied part tracking
- Supplier tracking for ordering

**Weaknesses:**
- Manual part entry
- No integration with eBay invoices
- No stock level checking

---

### **Workflow 5: SCHEDULING → Work Session Timer**
**Path:** Scheduling tab

**Test Steps:**
1. Change job state to "In Progress"
2. Click "Scheduling" tab
3. Click "⏰ Start Timer" button
4. Work for a few minutes
5. Click "⏸️ Pause Timer" button
6. Resume timer
7. Click "⏹️ Stop Timer" button
8. Verify work session created in list
9. Check start_time, end_time recorded
10. Verify duration_hours calculated
11. Check "actual_work_hours" field updates
12. Compare with "estimated_hours"
13. Check "remaining_hours" calculation
14. Check "completion_percentage"

**Expected Behavior:**
- ✅ Timer starts/stops correctly
- ✅ Work session records created
- ✅ Duration calculated in hours
- ✅ Actual work hours sum up
- ✅ Remaining hours = Estimated - Actual
- ✅ Completion % shows progress

**Failure Points:**
- ❌ Timer doesn't start
- ❌ Duration calculation wrong
- ❌ Work sessions don't save
- ❌ Actual hours don't sum
- ❌ Completion % doesn't update

**Strengths:**
- Live time tracking
- Multiple work sessions
- Progress monitoring
- Prevents forgotten time logging

**Weaknesses:**
- Requires manual start/stop
- No automatic pause detection
- Doesn't sync with labour lines

---

### **Workflow 6: INVOICE → Create & Post Invoice**
**Path:** Totals & Invoice tab

**Test Steps:**
1. Ensure labour and parts are added
2. Click "Totals & Invoice" tab
3. Verify financial calculations:
   - Labour Total = Sum of labour lines
   - Parts Total = Sum of parts lines
   - Subtotal = Labour + Parts
   - GST (10%) = Subtotal × 0.10
   - Grand Total = Subtotal + GST
4. Click "Quick Create Invoice" button
5. Verify invoice created
6. Check "Linked Invoice" field shows invoice
7. Click "View Invoice" to open it
8. Review invoice lines (labour + parts)
9. Return to job card
10. Click "✓ Post Invoice (Finalize)"
11. Verify invoice state changes to "Posted"
12. Verify job state changes to "Invoiced"

**Expected Behavior:**
- ✅ All calculations correct
- ✅ Invoice creates with all lines
- ✅ Labour lines transfer correctly
- ✅ Parts lines transfer correctly
- ✅ GST applies correctly (10%)
- ✅ Invoice links to job
- ✅ Job state updates

**Failure Points:**
- ❌ Calculations incorrect
- ❌ Invoice doesn't create
- ❌ Missing labour/parts lines
- ❌ GST wrong percentage
- ❌ Job state doesn't update
- ❌ Can't post invoice

**Strengths:**
- One-click invoice creation
- Auto-transfers all lines
- Proper GST handling
- State synchronization

**Weaknesses:**
- No quote approval workflow
- Can't edit invoice from job card
- No payment tracking on job card

---

### **Workflow 7: SERVICE HISTORY → View Previous Jobs**
**Path:** Service History tab

**Test Steps:**
1. Open job for vehicle with history
2. Click "Service History" tab
3. Verify previous jobs list appears
4. Check job details visible:
   - Job number
   - Date
   - Status
   - Hours worked
   - Labour/parts totals
   - Grand total
5. Click on a previous job to view details
6. Check for deferred work warning
7. Verify "deferred_work_notes" shows if applicable

**Expected Behavior:**
- ✅ Previous jobs for same vehicle show
- ✅ All details visible in list
- ✅ Can open previous jobs
- ✅ Deferred work highlighted
- ✅ Helpful for finding past issues

**Failure Points:**
- ❌ No previous jobs show
- ❌ Wrong vehicle's jobs show
- ❌ Can't open previous job
- ❌ Deferred work not showing

**Strengths:**
- Quick access to vehicle history
- Deferred work tracking
- Helps prevent repeat issues
- Good for warranty claims

**Weaknesses:**
- No search/filter in history
- No comparison between jobs
- Deferred work not auto-applied

---

### **Workflow 8: SCHEDULED MAINTENANCE → Auto-Suggest Services**
**Path:** Scheduled Maintenance tab

**Test Steps:**
1. Ensure odometer is set on job
2. Click "Scheduled Maintenance" tab
3. Check if suggested services appear
4. Review suggested service details:
   - Service name
   - Due at odometer reading
   - Estimated hours
   - Estimated cost
5. Click "Apply to Job" on a service
6. Verify labour lines added from template
7. Verify parts lines added from template
8. Check Labour tab for new lines
9. Check Parts tab for new lines
10. Verify totals updated

**Expected Behavior:**
- ✅ Services suggested based on odometer
- ✅ Service templates configured
- ✅ "Apply to Job" adds labour/parts
- ✅ All template items transfer
- ✅ Totals recalculate

**Failure Points:**
- ❌ No services suggested
- ❌ Service schedules not configured
- ❌ "Apply to Job" doesn't work
- ❌ Labour/parts don't transfer
- ❌ Totals don't update

**Strengths:**
- Proactive service suggestions
- Prevents missed maintenance
- Template-based (consistent)
- One-click application

**Weaknesses:**
- Requires pre-configured schedules
- Only based on odometer
- No time-based suggestions
- Manual application needed

---

## 📊 **COMPREHENSIVE TEST LOG TEMPLATE**

```markdown
# Workshop Browser Test Log

**Tester:** _______________
**Date:** _______________
**Browser:** Chrome (version: _______)
**Odoo Installation:** [ ] /workspace/addons [ ] Odoo19g [ ] Other: _______
**Odoo URL:** _______________
**Database:** _______________

---

## Environment Setup

- [ ] Odoo server running
- [ ] Workshop module installed
- [ ] Sample customer created
- [ ] Sample vehicle created
- [ ] Default labour rate configured ($120/hr)
- [ ] Service schedules configured (if testing Workflow 8)
- [ ] RapidAPI key configured (if testing Workflow 2)

---

## Workflow 1: BOOKING → Create New Job

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

### Test Results:
1. Job number generated: [ ] YES [ ] NO (Number: _______)
2. Customer dropdown: [ ] PASS [ ] FAIL
3. Vehicle dropdown: [ ] PASS [ ] FAIL
4. Date fields: [ ] PASS [ ] FAIL
5. Technician assignment: [ ] PASS [ ] FAIL
6. Save successful: [ ] PASS [ ] FAIL
7. State = "Booking": [ ] PASS [ ] FAIL

### Issues Found:
- _______________________________________________
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow1_new_job.png
- [ ] Attached: workflow1_saved.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 2: VEHICLE DETAILS → API Lookup

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED

### Test Results:
1. Registration field: [ ] PASS [ ] FAIL
2. State dropdown: [ ] PASS [ ] FAIL
3. API button visible: [ ] PASS [ ] FAIL
4. API call succeeds: [ ] PASS [ ] FAIL
5. Status message shown: [ ] PASS [ ] FAIL
6. Vehicle details populated: [ ] PASS [ ] FAIL

### API Response:
```
[Paste API response here]
```

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow2_lookup.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 3: LABOUR → Add Labour Lines

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

### Test Results:
1. Add line button: [ ] PASS [ ] FAIL
2. Inline editing: [ ] PASS [ ] FAIL
3. Default rate ($120): [ ] PASS [ ] FAIL (Rate: $______)
4. Subtotal calculation: [ ] PASS [ ] FAIL
   - 2.5 hrs × $120 = [ ] $300.00 [ ] Wrong: $______
5. Labour total: [ ] PASS [ ] FAIL (Total: $______)
6. Multiple lines: [ ] PASS [ ] FAIL
7. Save successful: [ ] PASS [ ] FAIL

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow3_labour.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 4: PARTS → Add Parts with Markup

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

### Test Results:
1. Add part line: [ ] PASS [ ] FAIL
2. Cost price field: [ ] PASS [ ] FAIL
3. Markup % field: [ ] PASS [ ] FAIL
4. Selling price calc: [ ] PASS [ ] FAIL
   - Cost $15 + 30% = [ ] $19.50 [ ] Wrong: $______
5. Quantity field: [ ] PASS [ ] FAIL
6. Subtotal calc: [ ] PASS [ ] FAIL
   - 5 × $19.50 = [ ] $97.50 [ ] Wrong: $______
7. Parts total: [ ] PASS [ ] FAIL (Total: $______)
8. Supplier dropdown: [ ] PASS [ ] FAIL
9. Customer-supplied flag: [ ] PASS [ ] FAIL

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow4_parts.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 5: SCHEDULING → Work Session Timer

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

### Test Results:
1. State change to "In Progress": [ ] PASS [ ] FAIL
2. Start Timer button: [ ] PASS [ ] FAIL
3. Timer starts: [ ] PASS [ ] FAIL (Time: _______)
4. Pause Timer button: [ ] PASS [ ] FAIL
5. Timer pauses: [ ] PASS [ ] FAIL
6. Resume works: [ ] PASS [ ] FAIL
7. Stop Timer button: [ ] PASS [ ] FAIL
8. Work session created: [ ] PASS [ ] FAIL
9. Duration calculated: [ ] PASS [ ] FAIL (Duration: ______ hrs)
10. Actual hours updated: [ ] PASS [ ] FAIL
11. Remaining hours: [ ] PASS [ ] FAIL
12. Completion %: [ ] PASS [ ] FAIL

### Timing Test:
- Started: _______
- Stopped: _______
- Expected duration: _______ minutes
- Actual duration recorded: _______ hours
- Accurate: [ ] YES [ ] NO

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow5_timer_start.png
- [ ] Attached: workflow5_timer_stop.png
- [ ] Attached: workflow5_sessions.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 6: INVOICE → Create & Post Invoice

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

### Test Results:
1. Labour total correct: [ ] PASS [ ] FAIL ($______)
2. Parts total correct: [ ] PASS [ ] FAIL ($______)
3. Subtotal correct: [ ] PASS [ ] FAIL ($______)
4. GST (10%) correct: [ ] PASS [ ] FAIL ($______)
5. Grand total correct: [ ] PASS [ ] FAIL ($______)
6. Create invoice button: [ ] PASS [ ] FAIL
7. Invoice created: [ ] PASS [ ] FAIL (Number: _______)
8. Labour lines transferred: [ ] PASS [ ] FAIL
9. Parts lines transferred: [ ] PASS [ ] FAIL
10. View invoice works: [ ] PASS [ ] FAIL
11. Post invoice button: [ ] PASS [ ] FAIL
12. Invoice posted: [ ] PASS [ ] FAIL
13. Job state = "Invoiced": [ ] PASS [ ] FAIL

### Financial Calculations:
```
Labour:     $______
Parts:      $______
Subtotal:   $______
GST (10%):  $______
TOTAL:      $______
```

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow6_totals.png
- [ ] Attached: workflow6_invoice.png
- [ ] Attached: workflow6_posted.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 7: SERVICE HISTORY → View Previous Jobs

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED (No history)

### Test Results:
1. Service History tab: [ ] PASS [ ] FAIL
2. Previous jobs shown: [ ] PASS [ ] FAIL (Count: _______)
3. Job details visible: [ ] PASS [ ] FAIL
4. Can open previous job: [ ] PASS [ ] FAIL
5. Deferred work warning: [ ] SHOWN [ ] NOT SHOWN [ ] N/A
6. Deferred notes visible: [ ] PASS [ ] FAIL [ ] N/A

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow7_history.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## Workflow 8: SCHEDULED MAINTENANCE → Auto-Suggest Services

**Start Time:** _______
**End Time:** _______
**Status:** [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED (No schedules)

### Test Results:
1. Odometer set: [ ] PASS [ ] FAIL (Reading: _______ km)
2. Maintenance tab: [ ] PASS [ ] FAIL
3. Services suggested: [ ] PASS [ ] FAIL (Count: _______)
4. Service details shown: [ ] PASS [ ] FAIL
5. "Apply to Job" button: [ ] PASS [ ] FAIL
6. Labour lines added: [ ] PASS [ ] FAIL (Count: _______)
7. Parts lines added: [ ] PASS [ ] FAIL (Count: _______)
8. Totals updated: [ ] PASS [ ] FAIL

### Suggested Services:
- Service 1: _______________________________________________
- Service 2: _______________________________________________

### Issues Found:
- _______________________________________________

### Screenshots:
- [ ] Attached: workflow8_suggestions.png
- [ ] Attached: workflow8_applied.png

### Strengths:
- _______________________________________________

### Weaknesses:
- _______________________________________________

---

## OVERALL TEST SUMMARY

### Pass/Fail Summary:
- Workflow 1 (Booking): [ ] PASS [ ] FAIL [ ] PARTIAL
- Workflow 2 (API Lookup): [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED
- Workflow 3 (Labour): [ ] PASS [ ] FAIL [ ] PARTIAL
- Workflow 4 (Parts): [ ] PASS [ ] FAIL [ ] PARTIAL
- Workflow 5 (Timer): [ ] PASS [ ] FAIL [ ] PARTIAL
- Workflow 6 (Invoice): [ ] PASS [ ] FAIL [ ] PARTIAL
- Workflow 7 (History): [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED
- Workflow 8 (Maintenance): [ ] PASS [ ] FAIL [ ] PARTIAL [ ] SKIPPED

### Critical Issues (Blockers):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Major Issues (Must Fix):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Minor Issues (Should Fix):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### System Ready for Production?
[ ] YES - All workflows pass
[ ] NO - See critical issues above
[ ] PARTIAL - Some workflows work

### Recommended Next Steps:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## STRENGTHS & WEAKNESSES ANALYSIS

### Overall Strengths:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Overall Weaknesses:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### User Experience Rating:
- Ease of Use: ____/10
- Speed: ____/10
- Reliability: ____/10
- Completeness: ____/10

### Would User Adopt This System?
[ ] YES - Ready for daily use
[ ] MAYBE - Needs improvements
[ ] NO - Too many issues

---

**Test Completed:** _______________ (Date/Time)
**Total Test Duration:** _______ hours
**Tester Signature:** _______________
```

---

## 🎯 **INSTRUCTIONS FOR BROWSER TESTING AGENT**

**YOU MUST:**

1. **Install & Access:**
   - Ensure Odoo is running
   - Open Chrome browser
   - Navigate to Odoo URL
   - Login with admin credentials

2. **Determine Installation:**
   - Check which workshop model is active
   - Report back: `workshop.workshop.job` or `workshop.job`?

3. **Prepare Test Data:**
   - Create 1 test customer
   - Create 1 test vehicle
   - Configure default labour rate

4. **Execute Each Workflow:**
   - Follow steps exactly
   - Take screenshots at every step
   - Note EVERY error or unexpected behavior
   - Fill in test log template

5. **Document Everything:**
   - Copy console errors (F12)
   - Note any freezing/slowness
   - Record calculation errors
   - Save all screenshots

6. **Complete Analysis:**
   - Fill strengths/weaknesses for each workflow
   - Provide overall recommendations
   - Rate production-readiness

7. **Report Back:**
   - Upload completed test log
   - Attach all screenshots
   - Summarize critical findings

---

## ⏱️ **ESTIMATED TIME: 3-4 hours**

- Setup: 30 minutes
- Workflow 1-3: 30 minutes each
- Workflow 4-6: 45 minutes each  
- Workflow 7-8: 20 minutes each
- Documentation: 30 minutes

---

**THIS IS THE MOST CRITICAL TEST - USER CANNOT USE SYSTEM UNTIL THIS PASSES!**
