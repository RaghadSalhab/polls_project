#version 1.0
#!/usr/bin/env python3
"""
Enhanced auto-seed script:
- Reads MySQL schema (INFORMATION_SCHEMA)
- Detects FK relationships
- Inserts fake data respecting constraints
"""

import mysql.connector
from faker import Faker
import random

CONFIG = {
    "host": "127.0.0.1",
    "port": 3308,
    "user": "local_user",
    "password": "local_pass",
    "database": "local_db",
    "rows_per_table": 10,
}

fake = Faker()

# Connect
conn = mysql.connector.connect(
    host=CONFIG["host"],
    port=CONFIG["port"],
    user=CONFIG["user"],
    password=CONFIG["password"],
    database=CONFIG["database"],
)
cursor = conn.cursor(dictionary=True)

print("🔎 Reading schema and relationships...")

# --- Get table list ---
cursor.execute(f"SHOW TABLES")
tables = [row[f"Tables_in_{CONFIG['database']}"] for row in cursor.fetchall()]

# --- Get FK relationships ---
cursor.execute("""
SELECT
  TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE
  TABLE_SCHEMA = %s AND
  REFERENCED_TABLE_NAME IS NOT NULL
""", (CONFIG["database"],))

fk_map = cursor.fetchall()

# Build dependency graph
dependencies = {}
for fk in fk_map:
    dependencies.setdefault(fk["TABLE_NAME"], []).append(fk["REFERENCED_TABLE_NAME"])

# Sort tables by dependency order
ordered_tables = []
visited = set()

def visit(table):
    if table in visited:
        return
    for dep in dependencies.get(table, []):
        visit(dep)
    visited.add(table)
    ordered_tables.append(table)

for t in tables:
    visit(t)

print("Insert order (FK-safe):", ordered_tables)

# --- Helper: get column info ---
def get_columns(table):
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, COLUMN_KEY, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    """, (CONFIG["database"], table))
    return cursor.fetchall()

# --- Helper: get all existing IDs from a table (for FK refs) ---
def get_existing_ids(table, col="id"):
    try:
        cursor.execute(f"SELECT {col} FROM {table}")
        return [r[col] for r in cursor.fetchall()]
    except:
        return []

# --- Clean tables before insert ---
for table in reversed(ordered_tables):
    print(f"🧹 Cleaning table: {table}")
    cursor.execute(f"SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute(f"SET FOREIGN_KEY_CHECKS=1;")
conn.commit()

# --- Insert fake data ---
for table in ordered_tables:
    cols = get_columns(table)
    print(f"\n⏳ Generating {CONFIG['rows_per_table']} rows for table: {table}")

    fk_rels = [fk for fk in fk_map if fk["TABLE_NAME"] == table]

    rows = []
    for _ in range(CONFIG["rows_per_table"]):
        row = {}
        for col in cols:
            name = col["COLUMN_NAME"]
            dtype = col["DATA_TYPE"]
            maxlen = col["CHARACTER_MAXIMUM_LENGTH"]
            extra = col["EXTRA"]

            # Skip auto_increment IDs
            if "auto_increment" in extra.lower():
                continue

            # If this column is a FK, choose random existing parent ID
            fk_match = next((fk for fk in fk_rels if fk["COLUMN_NAME"] == name), None)
            if fk_match:
                parent_ids = get_existing_ids(fk_match["REFERENCED_TABLE_NAME"], fk_match["REFERENCED_COLUMN_NAME"])
                row[name] = random.choice(parent_ids) if parent_ids else None
                continue

            # Generate fake data based on type
            if "char" in dtype or "text" in dtype:
                value = fake.word()
                if maxlen:
                    value = value[:maxlen]
            elif "int" in dtype:
                value = random.randint(1, 9999)
            elif "date" in dtype:
                value = fake.date()
            elif "decimal" in dtype or "float" in dtype or "double" in dtype:
                value = round(random.uniform(10, 999), 2)
            else:
                value = None
            row[name] = value
        rows.append(row)

    # Apply inserts
    if not rows:
        continue

    cols_names = list(rows[0].keys())
    cols_str = ", ".join(cols_names)
    placeholders = ", ".join(["%s"] * len(cols_names))
    insert_sql = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})"

    try:
        for r in rows:
            cursor.execute(insert_sql, list(r.values()))
        conn.commit()
        print(f"✅ Inserted data into {table}")
    except Exception as e:
        print(f"❌ Failed to insert into {table}: {e}")

print("\n🎉 Smart seeding complete!")
cursor.close()
conn.close()
