#!/usr/bin/env python3
import os
import subprocess
import time
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "my_poll_project"))
sys.path.insert(0, PROJECT_ROOT)

try:
    import settings.local as local_settings
except ImportError as e:
    print("❌ Could not import settings/local.py:", e)
    sys.exit(1)


DOCKER_CONTAINER = "mysql_dev"  
DUMP_DIR = "./db"
os.makedirs(DUMP_DIR, exist_ok=True)

def dump_db(db_name, db_user, db_pass):
    dump_file = os.path.join(DUMP_DIR, f"{db_name}.sql")
    cmd = [
        "docker", "exec", "-i", DOCKER_CONTAINER,
        "mysqldump",
        f"-u{db_user}",
        f"-p{db_pass}",
        "--no-data",  
        db_name
    ]

    print(f"🧩 Dumping schema for {db_name} ...")
    start = time.time()

    with open(dump_file, "w") as f:
        subprocess.run(cmd, stdout=f)

    duration = time.time() - start
    if os.path.exists(dump_file) and os.path.getsize(dump_file) > 0:
        print(f"✅ Dump saved to {dump_file} (⏱ {duration:.2f} sec)\n")
    else:
        print(f"❌ Failed to dump schema for {db_name}\n")

    return duration

if __name__ == "__main__":
    print("🚀 Starting schema dumps from Docker container...\n")
    total_start = time.time()
    total_duration = 0

    db_keys = getattr(local_settings, 'DATABASES', {})
    if not db_keys:
        print("❌ No DATABASES found in settings/local.py")
        sys.exit(1)

    for key, db_conf in db_keys.items():
        db_name = db_conf.get('NAME')
        db_user = db_conf.get('USER', 'root')
        db_pass = db_conf.get('PASSWORD', 'root')

        if db_name:
            total_duration += dump_db(db_name, db_user, db_pass)

    if 'shared' not in db_keys:
        default_conf = db_keys.get('default', {})
        print("ℹ️ Adding 'shared' schema manually based on default DB settings")
        total_duration += dump_db(
            'shared',
            default_conf.get('USER', 'root'),
            default_conf.get('PASSWORD', 'root')
        )

    total_end = time.time()
    total_elapsed = total_end - total_start

    print("🎉 All Docker database schemas dumped successfully!")
    print(f"⏱ Total time for all dumps: {total_elapsed:.2f} seconds")
