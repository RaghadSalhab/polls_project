#!/usr/bin/env python3
import subprocess
import os
import sys
import time

# -----------------------------
# Paths
# -----------------------------
SCRIPTS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)  # لضمان أن Python يجد settings.local

# -----------------------------
# Helper function
# -----------------------------
def run_script(cmd_list, description=""):
    print(f"\n🚀 Starting: {description}")
    start = time.time()
    try:
        subprocess.run(cmd_list, check=True)
        elapsed = time.time() - start
        print(f"✅ Done: {description} (⏱ {elapsed:.2f}s)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description}")
        print(e)
        sys.exit(1)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("🎬 Running all DB scripts in sequence...")

    # 1️⃣ Dump schemas from mysql_dev
    run_script(
        [sys.executable, os.path.join(SCRIPTS_DIR, "shared.py")],
        "Dump schemas from mysql_dev"
    )

    # 2️⃣ Import dumps into mysql_local
    # على Windows، bash قد لا يكون متاح، جرب Git Bash أو WSL
    run_script(
        ["python", os.path.join(SCRIPTS_DIR, "shared_loc.py")],
        "Import dumps into mysql_local"
    )


    # 3️⃣ Seed the databases
    run_script(
        [sys.executable, os.path.join(SCRIPTS_DIR, "shared_data.py")],
        "Seed databases with fake data"
    )

    print("\n🎉 All scripts executed successfully! Everything is ready ✅")
