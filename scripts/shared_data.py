#!/usr/bin/env python3
import mysql.connector
from faker import Faker
import random, os, time

# ==============================
# CONFIGURATION
# ==============================
CONFIG = {
    "host": "127.0.0.1",
    "port": 3308,          # MySQL local container port
    "user": "local_user",
    "password": "local_pass",
    "dump_dir": "./db",    # folder containing *.sql files (database names)
    "rows_per_table": 10,  # number of rows per table
    "use_ai": False,       # placeholder if using AI later
}

fake = Faker()

# ==============================
# HELPER FUNCTIONS
# ==============================
def seed_database(db_name):
    print(f"\n🧩 Seeding database: {db_name}")
    start_db_time = time.time()

    try:
        # Connect to DB
        conn = mysql.connector.connect(
            host=CONFIG["host"],
            port=CONFIG["port"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        # Use DB explicitly
        cursor.execute(f"USE `{db_name}`;")

        # Fetch tables
        cursor.execute("SHOW TABLES;")
        tables = [row[f"Tables_in_{db_name}"] for row in cursor.fetchall()]

        # Fetch foreign keys
        cursor.execute("""
            SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
        """, (db_name,))
        fk_map = cursor.fetchall()

        # Determine FK-safe insertion order
        dependencies = {}
        for fk in fk_map:
            dependencies.setdefault(fk["TABLE_NAME"], []).append(fk["REFERENCED_TABLE_NAME"])
        ordered_tables, visited = [], set()
        def visit(table):
            if table in visited: return
            for dep in dependencies.get(table, []):
                visit(dep)
            visited.add(table)
            ordered_tables.append(table)
        for t in tables: visit(t)

        # Helper: get table columns
        def get_columns(table):
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
            """, (db_name, table))
            return cursor.fetchall()

        # Helper: get existing IDs for FK columns with caching
        fk_cache = {}
        def get_existing_ids(table, col="id"):
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

        # Clean tables before seeding (disable FK checks once)
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in reversed(ordered_tables):
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()

        # Insert fake data
        for table in ordered_tables:
            cols = get_columns(table)
            fk_rels = [fk for fk in fk_map if fk["TABLE_NAME"] == table]
            rows = []

            for _ in range(CONFIG["rows_per_table"]):
                row = {}
                for col in cols:
                    name, dtype, maxlen, extra = col["COLUMN_NAME"], col["DATA_TYPE"], col["CHARACTER_MAXIMUM_LENGTH"], col["EXTRA"]
                    if "auto_increment" in extra.lower(): 
                        continue

                    # Foreign key
                    fk_match = next((fk for fk in fk_rels if fk["COLUMN_NAME"] == name), None)
                    if fk_match:
                        parent_ids = get_existing_ids(fk_match["REFERENCED_TABLE_NAME"], fk_match["REFERENCED_COLUMN_NAME"])
                        row[name] = random.choice(parent_ids) if parent_ids else None
                        continue

                    # Faker data
                    if "char" in dtype or "text" in dtype:
                        row[name] = fake.word()[:maxlen] if maxlen else fake.word()
                    elif "int" in dtype:
                        row[name] = random.randint(1, 9999)
                    elif "date" in dtype:
                        row[name] = fake.date()
                    elif "decimal" in dtype or "float" in dtype or "double" in dtype:
                        row[name] = round(random.uniform(10, 999), 2)
                    else:
                        row[name] = None
                rows.append(row)

            if rows:
                cols_str = ", ".join(rows[0].keys())
                placeholders = ", ".join(["%s"] * len(rows[0]))
                insert_sql = f"INSERT INTO `{table}` ({cols_str}) VALUES ({placeholders})"
                for r in rows:
                    cursor.execute(insert_sql, list(r.values()))
                conn.commit()
                print(f"✅ Inserted {CONFIG['rows_per_table']} rows into `{table}`")

        cursor.close()
        conn.close()
        db_time = time.time() - start_db_time
        print(f"⏱ Completed seeding `{db_name}` in {int(db_time)} seconds")

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
