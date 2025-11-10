#!/usr/bin/env python3
import os
import subprocess

DUMP_DIR = "./db"
CONTAINER = "mysql_local"
DB_USER = "root"
DB_PASS = "root"

print("🚀 Starting import of SQL dumps into local Docker MySQL...")
print(f"🔍 Source directory: {DUMP_DIR}")
print(f"🐳 Target container: {CONTAINER}\n")

for dump_file in os.listdir(DUMP_DIR):
    if not dump_file.endswith(".sql"):
        continue
    full_path = os.path.join(DUMP_DIR, dump_file)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No .sql dump files found: {full_path}")

    db_name = dump_file.replace(".sql", "")
    print(f"🧩 Creating database `{db_name}` inside container {CONTAINER} ...")
    subprocess.run([
        "docker", "exec", "-i", CONTAINER,
        "mysql", f"-u{DB_USER}", f"-p{DB_PASS}", "-e",
        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;"
    ], check=True)

    print(f"📥 Importing schema for `{db_name}` ...")
    with open(full_path, "rb") as f:
        subprocess.run([
            "docker", "exec", "-i", CONTAINER,
            "mysql", f"-u{DB_USER}", f"-p{DB_PASS}", db_name
        ], stdin=f, check=True)

print("\n🎉 All databases imported successfully!")
