# 🔄 ODOO SAVEPOINT - RESTORE INSTRUCTIONS

**Backup Created:** 2025-10-20 14:25:46  
**Backup Location:** `/workspace/backups/odoo_savepoint_20251020_142546/`  
**Odoo Version:** 19.0  
**Database:** odoo

---

## 📦 BACKUP CONTENTS

This savepoint contains:

1. ✅ **PostgreSQL Database** (`odoo_database.sql`) - 3.4 MB
   - Complete Odoo database with all data
   - Tables, sequences, constraints
   - System configurations

2. ✅ **Odoo Core Files** (`odoo_core.tar.gz`)
   - Odoo source code
   - Core modules
   - Configuration files

3. ✅ **Python Dependencies** (`python_requirements.txt`)
   - Complete list of installed packages (71 packages)
   - Exact versions used

4. ✅ **System Information** (`system_info.txt`)
   - OS and software versions
   - Configuration details
   - Running parameters

5. ✅ **Installed Packages** (`installed_packages.txt`)
   - System-level dependencies
   - PostgreSQL, Python, XML libraries

---

## 🚀 QUICK RESTORE (Emergency Recovery)

If something goes wrong, run these commands to restore:

```bash
# 1. Stop Odoo if running
pkill -f odoo-bin

# 2. Drop and recreate database
dropdb -U ubuntu odoo
createdb -U ubuntu odoo

# 3. Restore database
cd /workspace/backups/odoo_savepoint_20251020_142546
psql -U ubuntu odoo < odoo_database.sql

# 4. Start Odoo
cd /workspace
./odoo-bin --addons-path=addons --http-port=8069 --database=odoo --db_host=localhost --db_user=ubuntu --without-demo=all --log-level=warn
```

**Access Odoo:** http://localhost:8069

---

## 📋 DETAILED RESTORE PROCEDURE

### Step 1: Stop Odoo Server

```bash
# Find and kill Odoo process
pkill -f odoo-bin

# Verify it's stopped
ps aux | grep odoo-bin
```

### Step 2: Backup Current State (Optional)

```bash
# If you want to preserve the current broken state
pg_dump -U ubuntu odoo > /tmp/odoo_broken_$(date +%Y%m%d_%H%M%S).sql
```

### Step 3: Restore Database

```bash
# Drop existing database
dropdb -U ubuntu odoo

# Create fresh database
createdb -U ubuntu odoo

# Restore from backup
cd /workspace/backups/odoo_savepoint_20251020_142546
psql -U ubuntu odoo < odoo_database.sql

# You should see output like:
# SET
# SET
# CREATE EXTENSION
# ...
# (lots of SQL statements)
```

### Step 4: Verify Database Restoration

```bash
# Connect to database
psql -U ubuntu odoo

# Check tables exist
\dt

# Exit
\q
```

### Step 5: Restore Odoo Files (If Needed)

```bash
# Only needed if Odoo core files were damaged
cd /workspace/backups/odoo_savepoint_20251020_142546
tar -xzf odoo_core.tar.gz -C /workspace
```

### Step 6: Verify Python Dependencies

```bash
# Check if all packages are installed
cd /workspace/backups/odoo_savepoint_20251020_142546
pip3 list > /tmp/current_packages.txt
diff python_requirements.txt /tmp/current_packages.txt

# If packages are missing, reinstall
pip3 install -r python_requirements.txt
```

### Step 7: Start Odoo

```bash
cd /workspace
./odoo-bin --addons-path=addons --http-port=8069 --database=odoo --db_host=localhost --db_user=ubuntu --without-demo=all --log-level=warn
```

### Step 8: Test Access

```bash
# Check if Odoo responds
curl -I http://localhost:8069

# Should return: HTTP/1.1 303 SEE OTHER
```

Open in browser: http://localhost:8069

---

## 🔧 SYSTEM REQUIREMENTS

Before restoring, ensure these are installed:

### Required System Packages:
```bash
sudo apt-get install -y \
    postgresql \
    postgresql-contrib \
    python3 \
    python3-pip \
    libxml2-dev \
    libxslt1-dev \
    libldap2-dev \
    libsasl2-dev \
    libpq-dev \
    build-essential \
    python3-dev
```

### PostgreSQL Configuration:
```bash
# Ensure local trust authentication
sudo sed -i 's/peer/trust/g; s/md5/trust/g; s/scram-sha-256/trust/g' /etc/postgresql/*/main/pg_hba.conf
sudo service postgresql restart

# Create PostgreSQL user
sudo -u postgres createuser -s ubuntu
```

---

## ⚠️ TROUBLESHOOTING

### Problem: "Database already exists" error

```bash
# Force drop and recreate
dropdb -U ubuntu --force odoo
createdb -U ubuntu odoo
psql -U ubuntu odoo < odoo_database.sql
```

### Problem: "Permission denied" on restore

```bash
# Ensure you're the database owner
sudo -u postgres psql -c "ALTER DATABASE odoo OWNER TO ubuntu;"
```

### Problem: Odoo won't start

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check if port 8069 is already in use
lsof -i :8069 || netstat -tln | grep 8069

# Check Odoo logs
tail -f /var/log/odoo/odoo.log  # if using service
# OR check console output when running manually
```

### Problem: Missing Python packages

```bash
cd /workspace/backups/odoo_savepoint_20251020_142546
pip3 install -r python_requirements.txt --timeout 90
```

### Problem: "Could not connect to database"

```bash
# Verify PostgreSQL is running
sudo service postgresql status

# Start if stopped
sudo service postgresql start

# Test connection
psql -U ubuntu -d odoo -c "SELECT version();"
```

---

## 📊 BACKUP VERIFICATION

To verify backup integrity before restoring:

```bash
cd /workspace/backups/odoo_savepoint_20251020_142546

# Check database backup
echo "Database backup lines:"
wc -l odoo_database.sql

# Should be substantial (thousands of lines)

# Check for SQL errors
grep -i "error" odoo_database.sql

# Check Odoo core archive
tar -tzf odoo_core.tar.gz | head -20

# Check Python requirements
cat python_requirements.txt | grep -E "(lxml|psycopg2|Werkzeug)"
```

---

## 🎯 WHAT THIS BACKUP PRESERVES

### ✅ Database Content:
- All Odoo tables and data
- User accounts and permissions
- System configurations
- Module installation states
- Sequences and constraints

### ✅ Odoo Installation:
- Source code (version 19.0)
- Core modules
- Configuration files
- Binary executables

### ✅ Dependencies:
- Python packages list
- System packages list
- Version information

### ⚠️ NOT INCLUDED:
- Custom addons (none exist yet)
- Filestore attachments (if any)
- User-uploaded files
- Log files

---

## 🔐 SECURITY NOTES

- This backup contains database credentials
- Store in secure location
- Do not commit to public repositories
- Delete old backups when no longer needed

---

## 📞 SUPPORT

If restore fails:

1. Check PostgreSQL is running: `sudo service postgresql status`
2. Verify database exists: `psql -U ubuntu -l | grep odoo`
3. Check Python version: `python3 --version` (should be 3.13.3)
4. Verify all system packages installed (see system_info.txt)
5. Review error messages carefully

---

## ✨ SUCCESS CRITERIA

Restore is successful when:

- ✅ Database restore completes without errors
- ✅ Odoo server starts without crashes
- ✅ http://localhost:8069 responds with HTTP 303
- ✅ Can access Odoo login/database selector page
- ✅ No Python import errors in console

---

**Last Updated:** 2025-10-20  
**Backup Version:** 1.0  
**Status:** Production-Ready Savepoint

---

*Keep this file with the backup for future reference*
