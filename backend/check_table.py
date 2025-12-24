import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()

# List all clinic tables
print("📋 All clinic tables:")
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'clinic_%';")
tables = cursor.fetchall()
for table in tables:
    print(f"  - {table[0]}")

# Check vaccination table
print("\n🔍 Checking clinic_vaccination table:")
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'clinic_vaccination';")
result = cursor.fetchone()

if result:
    print("✅ clinic_vaccination EXISTS")
    cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'clinic_vaccination' ORDER BY ordinal_position;")
    columns = cursor.fetchall()
    print("\n📊 Columns:")
    for col in columns:
        print(f"  {col[0]}: {col[1]}")
else:
    print("❌ clinic_vaccination DOES NOT EXIST")