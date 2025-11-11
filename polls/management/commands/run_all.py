from django.core.management.base import BaseCommand
import subprocess
import os
import time
import sys

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "../../../scripts")
SCRIPTS_DIR = os.path.abspath(SCRIPTS_DIR)

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


class Command(BaseCommand):
    help = "Run all database dump/import/seed scripts in order."

    def handle(self, *args, **options):
        print("🎬 Running all DB scripts in sequence...")

        # 1️⃣ Dump schemas from mysql_dev
        run_script(
            ["python", os.path.join(SCRIPTS_DIR, "shared.py")],
            "Dump schemas from mysql_dev"
        )

        # 2️⃣ Import dumps into mysql_local
        run_script(
            ["bash", os.path.join(SCRIPTS_DIR, "import_to_local.sh")],
            "Import dumps into mysql_local"
        )

        # 3️⃣ Seed the databases
        run_script(
            ["python", os.path.join(SCRIPTS_DIR, "shared_data.py")],
            "Seed databases with fake data"
        )

        print("\n🎉 All scripts executed successfully! Everything is ready ✅")
