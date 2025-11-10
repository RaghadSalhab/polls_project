#!/usr/bin/env python3
import mysql.connector
from faker import Faker
import random, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    "max_workers": 6          
}

fake = Faker()

# ==============================
# HELPER: generate fake row
# ==============================
def generate_fake_row(columns, fk_map):
    row = {}
    for col in columns:
        name = col["Field"]
        dtype = col["Type"]
        extra = col.get("Extra", "")
        if "auto_increment" in extra.lower():
            continue
        if "int" in dtype:
            row[name] = random.randint(1, 9999)
        elif "char" in dtype or "text" in dtype:
            maxlen = int(''.join(filter(str.isdigit, dtype))) if any(c.isdigit() for c in dtype) else None
            val = fake.word()
            row[name] = val[:maxlen] if maxlen else val
        elif "date" in dtype:
            row[name] = fake.date()
        elif "decimal" in dtype or "float" in dtype or "double" in dtype:
            row[name] = round(random.uniform(10, 999), 2)
        else:
            row[name] = None
    return row

# ==============================
# Seed one database
# ==============================
def seed_database_optimized(db_name):
    start_time = time.time()
    try:
        conn = mysql.connector.connect(
            host=CONFIG["host"],
            port=CONFIG["port"],
            user=CONFIG["user"],
            password=CONFIG["password"],
            database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SHOW TABLES")
        tables = [row[f"Tables_in_{db_name}"] for row in cursor.fetchall()]

        for table in tables:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(f"TRUNCATE TABLE {table}")
            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()

        for table in tables:
            cursor.execute(f"SHOW COLUMNS FROM {table}")
            columns = cursor.fetchall()

            rows_data = []
            for _ in range(CONFIG["rows_per_table"]):
                row = generate_fake_row(columns, {})
                rows_data.append(list(row.values()))

            if rows_data:
                cols_str = ", ".join([c["Field"] for c in columns if "auto_increment" not in c.get("Extra","").lower()])
                placeholders = ", ".join(["%s"] * len(rows_data[0]))
                insert_sql = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})"
                cursor.executemany(insert_sql, rows_data)

            conn.commit()

        cursor.close()
        conn.close()

        db_time = time.time() - start_time
        print(f"✅ {db_name}: {len(tables)} tables seeded in {db_time:.1f}s")
        return db_time

    except Exception as e:
        print(f"❌ {db_name}: {e}")
        return 0

# ==============================
# Seed all databases in parallel
# ==============================
def seed_all_parallel():
    start_time = time.time()
    db_names = [f.replace("_dump.sql","") for f in os.listdir(CONFIG["dump_dir"]) if f.endswith("_dump.sql")]
    print(f"🚀 Seeding {len(db_names)} databases in parallel with {CONFIG['max_workers']} threads...")

    with ThreadPoolExecutor(max_workers=CONFIG["max_workers"]) as executor:
        futures = {executor.submit(seed_database_optimized, db): db for db in db_names}
        for future in as_completed(futures):
            db_name = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"❌ Failed {db_name}: {e}")

    total_time = time.time() - start_time
    print(f"\n🎉 All databases seeded in {total_time/60:.1f} minutes!")

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    seed_all_parallel()
