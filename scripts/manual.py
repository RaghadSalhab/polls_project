#!/usr/bin/env python3
import mysql.connector
import os
import csv

# ==============================
# CONFIGURATION
# ==============================
CONFIG = {
    "host": "127.0.0.1",
    "port": 3308,
    "user": "root",
    "password": "root",
    "manual_csv_dir": "./manual_data_csv",  
}

# ==============================
# HELPER FUNCTION
# ==============================
def seed_csv_data(csv_dir):
    if not os.path.exists(csv_dir):
        print(f"❌ CSV directory not found: {csv_dir}")
        return

    conn = mysql.connector.connect(
        host=CONFIG["host"],
        port=CONFIG["port"],
        user=CONFIG["user"],
        password=CONFIG["password"]
    )
    cursor = conn.cursor()

    for file_name in os.listdir(csv_dir):
        if not file_name.endswith(".csv"):
            continue

        db_table = file_name.replace(".csv", "")
        if "__" not in db_table:
            print(f"❌ Skipping {file_name}: invalid format, use <db_name>__<table_name>.csv")
            continue

        db_name, table_name = db_table.split("__")
        file_path = os.path.join(csv_dir, file_name)

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            cursor.execute(f"USE `{db_name}`;")
            for row in reader:
                columns = ", ".join(row.keys())
                placeholders = ", ".join(["%s"] * len(row))
                sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(row.values()))

        print(f"✅ Seeded {table_name} in {db_name}")

    conn.commit()
    cursor.close()
    conn.close()
    print("🎉 All CSV manual data inserted successfully!")

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    seed_csv_data(CONFIG["manual_csv_dir"])
