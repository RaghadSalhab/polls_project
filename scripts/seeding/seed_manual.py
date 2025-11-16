
# scripts/seeding/seed_manual.py
from db_helpers import connect_db, db_exists, table_exists
from config import CONFIG
import csv, os

def seed_manual(selected_files=None):
    csv_dir = CONFIG["manual_csv_dir"]

    if not os.path.exists(csv_dir):
        print(f"❌ CSV directory not found: {csv_dir}")
        return

    all_files = [
        f for f in os.listdir(csv_dir)
        if f.endswith(".csv")
    ]

    if selected_files:
        target_files = [f"{name}.csv" for name in selected_files if f"{name}.csv" in all_files]
        missing = set([f"{name}.csv" for name in selected_files]) - set(target_files)

        if missing:
            print(f"⚠️ These CSV manual files do NOT exist: {', '.join(missing)}")

    else:
        target_files = all_files  

    for file_name in target_files:
        db_table = file_name.replace(".csv", "")

        if "__" not in db_table:
            print(f"❌ Invalid file format: {file_name} (expected <db>__<table>)")
            continue

        db_name, table = db_table.split("__")

        if not db_exists(CONFIG, db_name):
            print(f"❌ Database `{db_name}` does not exist. Skipping…")
            continue

        conn, cursor = connect_db(CONFIG, db_name)

        if not table_exists(cursor, db_name, table):
            print(f"❌ Table `{table}` does not exist in `{db_name}`. Skipping…")
            conn.close()
            continue

        file_path = os.path.join(csv_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                cols = ", ".join(row.keys())
                placeholders = ", ".join(["%s"] * len(row))
                sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
                cursor.execute(sql, list(row.values()))

        conn.commit()
        conn.close()
        print(f"✅ Seeded `{table}` in `{db_name}`")

    print("🎉 Manual CSV seeding completed!")
