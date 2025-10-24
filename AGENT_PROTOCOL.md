# 🚨 CRITICAL AGENT PROTOCOL - WORKSHOP PROJECT

## PROBLEM DISCOVERED: Module was on Wrong Branch!

**Date:** Oct 24, 2025  
**Issue:** The entire `pg_motors_workshop` addon was built on a different branch and was NOT present on the main working branch.

**Root Cause:** Agents created the addon on branch `cursor/bc-a4f1f54b-44c0-464b-b0ad-d0021d57b2cf-00b5` but we were working on `cursor/keep-agents-on-project-track-2e7e`.

**Solution:** 
1. Identified the addon on the other branch using `git log` and `git show`
2. Checked out the files from that branch: `git checkout <commit> -- addons/pg_motors_workshop/`
3. Renamed from `pg_motors_workshop` to `workshop` (removed P&G ampersand symbol issue)
4. Updated ALL internal references using systematic find-and-replace

---

## 🔍 MANDATORY DEPENDENCY CHECK PROTOCOL

### Before Starting ANY Work:

#### 1. **CHECK WHAT BRANCH YOU'RE ON**
```bash
git branch
git status
```

#### 2. **CHECK IF FILES ACTUALLY EXIST**
```bash
ls -la /workspace/addons/workshop/
# Don't assume it exists - VERIFY IT!
```

#### 3. **CHECK FOR SPLIT BRANCHES**
```bash
# See all branches
git branch -a

# Check recent commits on all branches
git log --all --oneline --graph -20

# Search for your module in git history
git log --all --oneline --grep="workshop\|Workshop"
```

#### 4. **FIND LOST FILES**
```bash
# Find which commits have the files
git log --all --oneline -- addons/workshop/
git log --all --oneline -- addons/pg_motors_workshop/

# Show files in a specific commit
git show <commit-hash>:addons/workshop/__manifest__.py
```

---

## 📋 FILE-BY-FILE VERIFICATION PROTOCOL

### When Working on the Workshop Module:

**START HERE - Check these files exist IN ORDER:**

```bash
# 1. Module root
ls /workspace/addons/workshop/__manifest__.py
ls /workspace/addons/workshop/__init__.py
ls /workspace/addons/workshop/README.md

# 2. Models directory
ls /workspace/addons/workshop/models/__init__.py
ls /workspace/addons/workshop/models/customer.py
ls /workspace/addons/workshop/models/vehicle.py
ls /workspace/addons/workshop/models/vehicle_brand.py
ls /workspace/addons/workshop/models/workshop_job.py
ls /workspace/addons/workshop/models/job_labour.py
ls /workspace/addons/workshop/models/job_parts.py
ls /workspace/addons/workshop/models/vendor_invoice_ocr.py
ls /workspace/addons/workshop/models/mail_thread_invoice_ocr.py
ls /workspace/addons/workshop/models/res_config_settings.py

# 3. Views directory
ls /workspace/addons/workshop/views/menu_views.xml
ls /workspace/addons/workshop/views/customer_views.xml
ls /workspace/addons/workshop/views/vehicle_views.xml
ls /workspace/addons/workshop/views/workshop_job_views.xml
ls /workspace/addons/workshop/views/job_labour_views.xml
ls /workspace/addons/workshop/views/job_parts_views.xml
ls /workspace/addons/workshop/views/vendor_invoice_ocr_views.xml
ls /workspace/addons/workshop/views/res_config_settings_views.xml

# 4. Security
ls /workspace/addons/workshop/security/workshop_security.xml
ls /workspace/addons/workshop/security/ir.model.access.csv

# 5. Reports
ls /workspace/addons/workshop/reports/job_invoice_report.xml
ls /workspace/addons/workshop/reports/workshop_reports.xml

# 6. Wizards
ls /workspace/addons/workshop/wizards/mysql_import_wizard.py
ls /workspace/addons/workshop/wizards/mysql_import_wizard_views.xml

# 7. Data
ls /workspace/addons/workshop/data/vehicle_brands_data.xml
ls /workspace/addons/workshop/data/service_types_data.xml
```

**IF ANY FILE IS MISSING:**
1. **STOP IMMEDIATELY**
2. Check git branches for the file
3. Find which branch has it
4. Restore it before continuing

---

## 🔧 DEPENDENCY VERIFICATION PROTOCOL

### Check Dependencies Match Reality:

#### 1. **Read __manifest__.py First**
```python
# Check what the manifest SAYS it depends on
cat /workspace/addons/workshop/__manifest__.py | grep "depends"
```

#### 2. **Check What Files ACTUALLY Import**
```bash
# Search all Python files for imports
grep -r "^from odoo" /workspace/addons/workshop/models/*.py
grep -r "^import odoo" /workspace/addons/workshop/models/*.py

# Check for external library imports
grep -r "^import " /workspace/addons/workshop/models/*.py | grep -v "from odoo"
```

#### 3. **Verify External Dependencies Exist**
```bash
# If manifest says: 'external_dependencies': {'python': ['PyPDF2']}
# Then verify:
python3 -c "import PyPDF2; print('PyPDF2 installed')"
```

#### 4. **Check Model References**
```bash
# Find all model references in code
grep -r "self\.env\[" /workspace/addons/workshop/models/*.py
grep -r "Many2one\(" /workspace/addons/workshop/models/*.py
grep -r "One2many\(" /workspace/addons/workshop/models/*.py

# Make sure those models exist or are in dependencies
```

#### 5. **Verify View References**
```bash
# Check that models referenced in views actually exist
grep -r 'model="' /workspace/addons/workshop/views/*.xml

# Check each model name matches a Python file
# workshop.customer -> models/customer.py with _name = 'workshop.customer'
```

---

## ⚠️ COMMON MISTAKES TO AVOID

### 1. **Assuming Files Exist**
❌ BAD: "I'll modify the workshop addon..."  
✅ GOOD: "Let me first verify the workshop addon exists: `ls /workspace/addons/workshop/`"

### 2. **Not Checking Git Branches**
❌ BAD: "The file doesn't exist, I'll create it"  
✅ GOOD: "File missing. Let me check if it's on another branch: `git log --all -- path/to/file`"

### 3. **Ignoring Model Name Mismatches**
❌ BAD: Model file `customer.py` with `_name = 'pg.motors.customer'` but views reference `'workshop.customer'`  
✅ GOOD: Verify model `_name` matches ALL references in views, security, and other models

### 4. **Not Testing Imports**
❌ BAD: Assuming code will work  
✅ GOOD: Test Python syntax: `python3 -m py_compile /workspace/addons/workshop/models/*.py`

### 5. **Creating Duplicate Modules**
❌ BAD: "workshop doesn't exist, I'll create a new one"  
✅ GOOD: Search ALL branches first: `git log --all --oneline -- addons/workshop/`

---

## 🎯 SYSTEMATIC WORKFLOW FOR ALL AGENTS

### Phase 1: DISCOVERY (ALWAYS DO THIS FIRST)
1. Check current branch
2. Check if module directory exists
3. Search git history for module
4. Identify correct branch with latest code
5. Document findings

### Phase 2: VERIFICATION
1. List all files that should exist
2. Verify each file exists
3. Read __manifest__.py dependencies
4. Check imports in all .py files
5. Verify model names match references
6. Test Python syntax

### Phase 3: CONSISTENCY CHECK
1. Search for old naming (pg.motors, pg_motors, P&G)
2. Verify all renamed to new naming (workshop)
3. Check security file references
4. Check view model references
5. Check data file references

### Phase 4: INTEGRATION TEST
1. Try to import the module in Python
2. Check for missing dependencies
3. Install missing dependencies if needed
4. Verify no circular imports

### Phase 5: COMMIT
1. Stage all files
2. Commit with descriptive message
3. Verify commit succeeded
4. Check git status is clean

---

## 📝 CHECKLIST FOR EVERY WORK SESSION

**Copy this checklist and check off each item:**

- [ ] I am on the correct branch
- [ ] I verified the workshop addon exists at `/workspace/addons/workshop/`
- [ ] I checked git history for any split branches
- [ ] I read the `__manifest__.py` file completely
- [ ] I verified all dependencies are correct
- [ ] I checked model names match in all files
- [ ] I searched for any old naming (pg.motors, pg_motors, P&G)
- [ ] I tested Python imports compile without errors
- [ ] I verified no circular dependencies
- [ ] I checked the current git status
- [ ] If I created/modified files, I committed them immediately

---

## 🔴 RED FLAGS - STOP AND INVESTIGATE

If you see any of these, **STOP WORK** and investigate:

1. **"File not found" errors** - Check git branches
2. **"Module not found" when importing** - Check dependencies
3. **Model name mismatches** - Old naming still present
4. **Empty directories** - Files on different branch
5. **Import errors** - Missing external dependencies
6. **Reference errors in views** - Model names don't match
7. **Security access errors** - Group names don't match
8. **"Nothing to commit" when you just created files** - Already committed or wrong branch

---

## 🎓 LESSONS LEARNED FROM THIS INCIDENT

### What Went Wrong:
1. Agents worked on different branches without realizing it
2. No one checked if the addon actually existed before trying to modify it
3. No systematic file verification was done
4. Git branch awareness was missing

### What Saved Us:
1. Checking git log with `--all` flag
2. Using `git show` to inspect files on other branches
3. Systematic search for the lost addon
4. Proper renaming and consistency checks

### Prevention:
1. **ALWAYS** verify files exist before modifying
2. **ALWAYS** check which branch you're on
3. **ALWAYS** search git history when files are missing
4. **ALWAYS** verify naming consistency
5. **ALWAYS** test imports before committing

---

## 🚀 CURRENT STATE (Oct 24, 2025)

**Branch:** `cursor/keep-agents-on-project-track-2e7e`

**Module Name:** `workshop` (previously `pg_motors_workshop`)

**Location:** `/workspace/addons/workshop/`

**Status:** ✅ All files present, renamed, and ready

**Models:**
- `workshop.customer`
- `workshop.vehicle`
- `workshop.vehicle.brand`
- `workshop.workshop.job`
- `workshop.job.labour`
- `workshop.job.parts`
- `vendor.invoice.ocr`

**Dependencies:**
- base, mail, account, stock, fleet, contacts, product, sale_management, web
- External: PyPDF2

**Next Steps:**
1. Install PyPDF2 if missing: `pip install PyPDF2`
2. Install module in Odoo
3. Continue development with proper verification

---

## 📞 COMMUNICATION PROTOCOL

**Before saying "the file doesn't exist":**
1. Check current branch
2. Search all branches
3. Report which branch it's on (if any)

**Before saying "I'll create a new file":**
1. Search git history
2. Check if it already exists somewhere
3. Restore if found, only create if truly new

**Before saying "the module is broken":**
1. Verify you're looking at the right branch
2. Check if files are present
3. Verify dependencies
4. Test imports

---

## ✅ SUCCESS CRITERIA

**You know you're doing it right when:**
- You check branch FIRST, before every task
- You verify files exist before modifying
- You search git when files are missing
- You test imports after changes
- You commit immediately after successful changes
- You use this checklist every time

---

**REMEMBER:** The workshop addon exists NOW at `/workspace/addons/workshop/` on the main branch. Don't recreate it. Don't assume it's missing. Verify first, then work.

---

*This protocol was created after discovering the workshop addon was on a different branch. Follow it to prevent similar issues.*
