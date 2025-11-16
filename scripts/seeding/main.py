# scripts/seeding/main.py

import os
import sys
import time
from config import CONFIG
from db_helpers import connect_db, get_tables, get_foreign_keys, get_columns, db_exists
from seed_manual import seed_manual
from seeder_auto import determine_insert_order, seed_table

def seed_database(db_name):
    print(f"\n🧩 Seeding database: {db_name}")
    start_time = time.time()

    if not db_exists(CONFIG, db_name):
        print(f"❌ Database `{db_name}` does not exist. Skipping…")
        return

    try:
        conn, cursor = connect_db(CONFIG, db_name)
        tables = get_tables(cursor, db_name)
        fk_map = get_foreign_keys(cursor, db_name)
        ordered_tables = determine_insert_order(tables, fk_map)

        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        for table in reversed(ordered_tables):
            cursor.execute(f"TRUNCATE TABLE `{table}`;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()

        for table in ordered_tables:
            columns = get_columns(cursor, db_name, table)
            seed_table(cursor, db_name, table, columns, fk_map, CONFIG["rows_per_table"])

        conn.commit()
        cursor.close()
        conn.close()

        print(f"⏱ Completed seeding `{db_name}` in {int(time.time() - start_time)} seconds")

    except Exception as e:
        print(f"❌ Failed to seed `{db_name}`: {e}")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("\nUsage:")
        print(" python scripts/seeding/main.py fake")
        print(" python scripts/seeding/main.py manual")
        print(" python scripts/seeding/main.py manual file1 file2 file3")
        print(" python scripts/seeding/main.py both")
        sys.exit(1)

    mode = sys.argv[1]
    manual_files = sys.argv[2:] if len(sys.argv) > 2 else None

    start_time = time.time()

    # ---------- AUTO FAKE ----------
    if mode in ("fake", "both"):
        for dump_file in os.listdir(CONFIG["dump_dir"]):
            if dump_file.endswith(".sql"):
                db_name = dump_file.replace(".sql", "")
                seed_database(db_name)

    # ---------- MANUAL ----------
    if mode in ("manual", "both"):
        seed_manual(manual_files)

    total = int(time.time() - start_time)
    print(f"\n🎉 Completed! Total time: {total} seconds")
