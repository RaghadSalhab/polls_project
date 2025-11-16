#!/usr/bin/env python3
# scripts/seed_shared.py

import mysql.connector
from faker import Faker
import random
import os
import time

# ==============================
# CONFIGURATION
# ==============================
CONFIG = {
    "host": "127.0.0.1",
    "port": 3308,
    "user": "local_user",
    "password": "local_pass",
    "dump_dir": "./db",
    "rows_per_table": 10,
    "use_ai": False,
}

fake = Faker()

# ==============================
# DATABASE HELPERS
# ==============================
def connect_db(db_name):
    conn = mysql.connector.connect(
        host=CONFIG["host"],
        port=CONFIG["port"],
        user=CONFIG["user"],
        password=CONFIG["password"],
        database=db_name
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor


def get_tables(cursor, db_name):
    cursor.execute("SHOW TABLES;")
    return [row[f"Tables_in_{db_name}"] for row in cursor.fetchall()]


def get_foreign_keys(cursor, db_name):
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA=%s AND REFERENCED_TABLE_NAME IS NOT NULL
    """, (db_name,))
    return cursor.fetchall()


def get_columns(cursor, db_name, table):
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
    """, (db_name, table))
    return cursor.fetchall()


def get_existing_ids(cursor, table, col="id", fk_cache=None):
    fk_cache = fk_cache if fk_cache is not None else {}
    key = f"{table}.{col}"
    if key in fk_cache:
        return fk_cache[key]

    try:
        cursor.execute(f"SELECT {col} FROM `{table}`;")
        ids = [r[col] for r in cursor.fetchall()]
        fk_cache[key] = ids
        return ids
    except:
        fk_cache[key] = []
        return []


def generate_fake_value(col_info, fk_match=None, existing_ids=None):
    name = col_info["COLUMN_NAME"]
    dtype = col_info["DATA_TYPE"]
    maxlen = col_info["CHARACTER_MAXIMUM_LENGTH"]
    extra = col_info["EXTRA"]

    if "auto_increment" in extra.lower():
        return None

    # Foreign key
    if fk_match and existing_ids:
        return random.choice(existing_ids) if existing_ids else None

    # Boolean / small int
    if "tinyint" in dtype:
        return random.randint(0, 1)
    # String/text
    elif "char" in dtype or "text" in dtype:
        return fake.word()[:maxlen] if maxlen else fake.word()
    # Integer
    elif "int" in dtype:
        return random.randint(1, 9999)
    # Decimal / float
    elif "decimal" in dtype or "float" in dtype or "double" in dtype:
        return round(random.uniform(10, 999), 2)
    # Date
    elif "date" in dtype:
        return fake.date()
    else:
        return None


def determine_insert_order(tables, fk_map):
    dependencies = {}
    for fk in fk_map:
        dependencies.setdefault(fk["TABLE_NAME"], []).append(fk["REFERENCED_TABLE_NAME"])

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

    return ordered_tables

def seed_table(cursor, db_name, table, columns, fk_map):
    fk_rels = [fk for fk in fk_map if fk["TABLE_NAME"] == table]
    fk_cache = {}
    rows = []

    # نحتفظ بالقيم الفريدة لتجنب Duplicate entry
    unique_rows = set()

    for _ in range(CONFIG["rows_per_table"] * 5):  # نحاول أكثر من مرة لتوليد قيم مختلفة
        row = {}
        for col in columns:
            fk_match = next((fk for fk in fk_rels if fk["COLUMN_NAME"] == col["COLUMN_NAME"]), None)
            existing_ids = get_existing_ids(cursor, fk_match["REFERENCED_TABLE_NAME"],
                                            fk_match["REFERENCED_COLUMN_NAME"], fk_cache) if fk_match else None
            value = generate_fake_value(col, fk_match, existing_ids)
            if value is not None:
                row[col["COLUMN_NAME"]] = value

        # إنشاء tuple للقيم الفريدة حسب كل جدول
        row_tuple = tuple(row.items())
        if row_tuple not in unique_rows:
            unique_rows.add(row_tuple)
            rows.append(row)
        if len(rows) >= CONFIG["rows_per_table"]:
            break

    if rows:
        cols_str = ", ".join(rows[0].keys())
        placeholders = ", ".join(["%s"] * len(rows[0]))
        insert_sql = f"INSERT INTO `{table}` ({cols_str}) VALUES ({placeholders})"
        for r in rows:
            cursor.execute(insert_sql, list(r.values()))
        print(f"✅ Inserted {len(rows)} rows into `{table}`")

def seed_database(db_name):
    print(f"\n🧩 Seeding database: {db_name}")
    start_time = time.time()
    try:
        conn, cursor = connect_db(db_name)
        tables = get_tables(cursor, db_name)
        fk_map = get_foreign_keys(cursor, db_name)
        ordered_tables = determine_insert_order(tables, fk_map)

        # Clean tables first
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in reversed(ordered_tables):
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()

        # Seed each table
        for table in ordered_tables:
            columns = get_columns(cursor, db_name, table)
            seed_table(cursor, db_name, table, columns, fk_map)
        conn.commit()

        cursor.close()
        conn.close()
        print(f"⏱ Completed seeding `{db_name}` in {int(time.time() - start_time)} seconds")

    except Exception as e:
        print(f"❌ Failed to seed `{db_name}`: {e}")


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    start_time = time.time()
    for dump_file in os.listdir(CONFIG["dump_dir"]):
        if dump_file.endswith(".sql"):
            db_name = dump_file.replace(".sql", "")
            seed_database(db_name)

    total_time = time.time() - start_time
    minutes, seconds = divmod(int(total_time), 60)
    print(f"\n🎉 All databases seeded successfully! ⏱ Total time: {minutes} min {seconds} sec")
