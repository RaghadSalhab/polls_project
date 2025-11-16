# scripts/seeding/seeder_auto.py
from db_helpers import get_existing_ids
from faker import Faker
import random

fake = Faker()

def generate_fake_value(col_info, fk_match=None, existing_ids=None):
    dtype = col_info["DATA_TYPE"]
    maxlen = col_info["CHARACTER_MAXIMUM_LENGTH"]
    extra = col_info["EXTRA"]

    if "auto_increment" in extra.lower():
        return None

    if fk_match and existing_ids:
        return random.choice(existing_ids) if existing_ids else None

    if "tinyint" in dtype:
        return random.randint(0, 1)
    elif "char" in dtype or "text" in dtype:
        return fake.word()[:maxlen] if maxlen else fake.word()
    elif "int" in dtype:
        return random.randint(1, 9999)
    elif "decimal" in dtype or "float" in dtype or "double" in dtype:
        return round(random.uniform(10, 999), 2)
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

def seed_table(cursor, db_name, table, columns, fk_map, rows_per_table):
    fk_rels = [fk for fk in fk_map if fk["TABLE_NAME"] == table]
    fk_cache = {}
    rows = []
    unique_rows = set()

    for _ in range(rows_per_table * 5):
        row = {}
        for col in columns:
            fk_match = next((fk for fk in fk_rels if fk["COLUMN_NAME"] == col["COLUMN_NAME"]), None)
            existing_ids = get_existing_ids(cursor, fk_match["REFERENCED_TABLE_NAME"],
                                            fk_match["REFERENCED_COLUMN_NAME"], fk_cache) if fk_match else None
            value = generate_fake_value(col, fk_match, existing_ids)
            if value is not None:
                row[col["COLUMN_NAME"]] = value

        row_tuple = tuple(row.items())
        if row_tuple not in unique_rows:
            unique_rows.add(row_tuple)
            rows.append(row)
        if len(rows) >= rows_per_table:
            break

    if rows:
        cols_str = ", ".join(rows[0].keys())
        placeholders = ", ".join(["%s"] * len(rows[0]))
        insert_sql = f"INSERT INTO `{table}` ({cols_str}) VALUES ({placeholders})"
        for r in rows:
            cursor.execute(insert_sql, list(r.values()))
        print(f"✅ Inserted {len(rows)} rows into `{table}`")
