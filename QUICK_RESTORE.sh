#!/bin/bash
# EMERGENCY ODOO RESTORE SCRIPT
# Run this if you need to restore from savepoint

echo "🔄 ODOO EMERGENCY RESTORE"
echo "========================"
echo ""
echo "This will restore Odoo to the savepoint from 2025-10-20 14:25:46"
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

echo ""
echo "1️⃣ Stopping Odoo..."
pkill -f odoo-bin
sleep 2

echo "2️⃣ Dropping database..."
dropdb -U ubuntu odoo 2>/dev/null || true

echo "3️⃣ Creating fresh database..."
createdb -U ubuntu odoo

echo "4️⃣ Restoring database..."
psql -U ubuntu odoo < /workspace/backups/odoo_savepoint_20251020_142546/odoo_database.sql > /dev/null 2>&1

echo "5️⃣ Starting Odoo..."
cd /workspace
nohup ./odoo-bin --addons-path=addons --http-port=8069 --database=odoo \
  --db_host=localhost --db_user=ubuntu --without-demo=all --log-level=warn > /tmp/odoo.log 2>&1 &

echo ""
echo "✅ RESTORE COMPLETE!"
echo ""
echo "Odoo is starting... wait 10 seconds then access:"
echo "http://localhost:8069"
echo ""
echo "Check logs: tail -f /tmp/odoo.log"
