# ⚡ BROWSER TEST QUICK START GUIDE

**For:** Agent with Chrome browser access  
**Time Required:** 3-4 hours  
**Status:** CRITICAL - BLOCKING ALL OTHER WORK

---

## 🚀 QUICK START (5 Minutes)

### Step 1: Open Odoo
```bash
# Open Chrome
# Navigate to: http://localhost:8069 (or your Odoo URL)
# Login as: admin
```

### Step 2: Find Workshop Module
```
Main Menu → Workshop (look for wrench icon)
If not visible → Apps → Search "Workshop" → Install
```

### Step 3: Check Which Version
```
Workshop → Job Cards → Open any job
Look at browser URL:
  - Contains "workshop.workshop.job" = Version 1 (/workspace)
  - Contains "workshop.job" = Version 2 (Odoo19g)
  
REPORT WHICH ONE YOU SEE!
```

---

## 📋 THE 8 WORKFLOWS TO TEST

### ✅ **Quick Checklist** (Check as you go)

- [ ] **Workflow 1:** Create new job → Job number generated?
- [ ] **Workflow 2:** API vehicle lookup → Details populate?
- [ ] **Workflow 3:** Add labour → Calculations correct?
- [ ] **Workflow 4:** Add parts with markup → Math works?
- [ ] **Workflow 5:** Start/stop timer → Sessions record?
- [ ] **Workflow 6:** Create invoice → PDF generates?
- [ ] **Workflow 7:** View service history → Previous jobs show?
- [ ] **Workflow 8:** Suggest maintenance → Services apply?

---

## 🎯 **WHAT YOU'RE LOOKING FOR**

### ✅ **GOOD Signs:**
- Buttons work when clicked
- Forms save without errors
- Calculations happen automatically
- Numbers add up correctly
- States/statuses update
- PDF generates
- No console errors (F12)

### ❌ **BAD Signs:**
- Buttons do nothing
- "Server Error" messages
- Calculations wrong or missing
- Can't save forms
- Fields don't populate
- Console shows red errors
- Page freezes/hangs

---

## 📸 **SCREENSHOT REQUIREMENTS**

**Take screenshots of:**
1. New job form (before save)
2. Job number after save
3. Labour tab with lines added
4. Parts tab with markup calculator
5. Timer running
6. Financial totals
7. Invoice created
8. Any errors you encounter

**How to screenshot:**
- Windows: Win + Shift + S
- Mac: Cmd + Shift + 4
- Chrome: F12 → Network tab (for API errors)

---

## 🔧 **SAMPLE TEST DATA**

Use this for consistency:

**Customer:**
- Name: Test Customer
- Phone: 0412345678
- Email: test@example.com

**Vehicle:**
- Rego: TEST123
- Make: Toyota
- Model: Camry
- Year: 2020
- Odometer: 50,000 km

**Labour Line:**
- Description: "Full service - Oil, filters, inspection"
- Hours: 2.5
- Rate: $120.00
- Expected Total: $300.00

**Parts Line:**
- Description: "Engine Oil 5W-30"
- Part #: OIL-5W30-5L
- Cost: $15.00
- Markup: 30%
- Expected Selling: $19.50
- Quantity: 5
- Expected Total: $97.50

**Expected Invoice Total:**
- Labour: $300.00
- Parts: $97.50
- Subtotal: $397.50
- GST (10%): $39.75
- **TOTAL: $437.25**

---

## ⚠️ **CRITICAL ISSUES TO CHECK**

### 1. **Job Number Generation**
- Does it auto-generate (e.g., WS00001)?
- Is it unique?
- Can you save without it?

### 2. **Calculations**
```
Labour: Hours × Rate = Subtotal ✓
Parts: (Cost × (1 + Markup%)) × Qty = Subtotal ✓
Total: Labour + Parts = Subtotal ✓
GST: Subtotal × 0.10 = GST Amount ✓
Grand: Subtotal + GST = Grand Total ✓
```

### 3. **Invoice Creation**
- One-click create works?
- All labour lines transfer?
- All parts lines transfer?
- Totals match job card?
- Can post/finalize invoice?

### 4. **Timer Functionality**
- Start button works?
- Pause button works?
- Stop button works?
- Duration records correctly?
- Multiple sessions possible?

---

## 📝 **REPORT TEMPLATE**

```markdown
# Browser Test Report

## Environment
- Odoo URL: _____________
- Workshop Version: [ ] workshop.workshop.job [ ] workshop.job
- Browser: Chrome _______
- Date: _____________

## Quick Results
- Workflow 1 (Booking): ✅ PASS / ❌ FAIL
- Workflow 2 (API): ✅ PASS / ❌ FAIL / ⏭️ SKIP
- Workflow 3 (Labour): ✅ PASS / ❌ FAIL
- Workflow 4 (Parts): ✅ PASS / ❌ FAIL
- Workflow 5 (Timer): ✅ PASS / ❌ FAIL
- Workflow 6 (Invoice): ✅ PASS / ❌ FAIL
- Workflow 7 (History): ✅ PASS / ❌ FAIL / ⏭️ SKIP
- Workflow 8 (Maintenance): ✅ PASS / ❌ FAIL / ⏭️ SKIP

## Critical Issues Found
1. _______________________________
2. _______________________________
3. _______________________________

## System Ready?
[ ] YES - Works perfectly
[ ] MOSTLY - Minor issues only
[ ] NO - Major problems

## Screenshots
[Attach all screenshots here]
```

---

## 🆘 **IF YOU GET STUCK**

### Common Issues:

**"Workshop menu not visible"**
→ Go to Apps, search "Workshop", click Install

**"Job won't save"**
→ Check console (F12) for red errors
→ Screenshot the error
→ Try filling ALL required fields

**"Calculations don't work"**
→ Try typing a number and pressing Tab
→ Try saving the record
→ Check if JavaScript errors in console

**"Can't find button"**
→ Try scrolling down
→ Try different tabs
→ Check if state needs to change first

**"Invoice won't create"**
→ Ensure labour OR parts exist
→ Check if job state allows invoice
→ Look for error messages

---

## ⏱️ **TIME BUDGET**

```
Setup & Environment Check: 30 min
Workflow 1 (Booking):     30 min
Workflow 2 (API):         20 min
Workflow 3 (Labour):      30 min
Workflow 4 (Parts):       30 min
Workflow 5 (Timer):       45 min
Workflow 6 (Invoice):     45 min
Workflow 7 (History):     15 min
Workflow 8 (Maintenance): 15 min
Documentation:            30 min
─────────────────────────────────
TOTAL:                  4 hours
```

---

## 🎯 **SUCCESS CRITERIA**

**Minimum to Pass:**
- ✅ Can create job with job number
- ✅ Can add labour (calculations work)
- ✅ Can add parts (calculations work)
- ✅ Can create invoice
- ✅ Financial totals correct

**Bonus Points:**
- ✅ Timer works
- ✅ API lookup works
- ✅ Service history shows
- ✅ Maintenance suggestions work

**Instant Fail:**
- ❌ Can't create job at all
- ❌ Can't save labour/parts
- ❌ Calculations completely wrong
- ❌ Can't create invoice
- ❌ System crashes/freezes

---

## 📞 **NEXT STEPS AFTER TESTING**

1. **If ALL PASS:** 
   - Report: "System ready for production"
   - User can start using it immediately
   - Move to training phase

2. **If MOSTLY PASS:**
   - Report issues found
   - Developer fixes issues
   - Re-test failed workflows only

3. **If MAJOR FAILS:**
   - Stop testing
   - Report critical blockers
   - Wait for fixes
   - Re-test everything

---

**REMEMBER:** You're testing if a **real mechanic** can use this daily. If YOU can't figure it out, THEY can't either!

**BE HONEST:** If it's broken, say it's broken. Better to find bugs now than after user starts using it!

---

**Full details:** See `/workspace/CRITICAL_BROWSER_TEST_PLAN.md`
