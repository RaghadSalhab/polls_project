import os
import time
import socket
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Sync LocalStack dev_db to local_db reliably, with dummy data"

    def wait_for_mysql(self, host, port, timeout=30):
        """انتظار MySQL ليشتغل قبل أي restore"""
        start = time.time()
        while True:
            try:
                s = socket.create_connection((host, port), timeout=2)
                s.close()
                return True
            except Exception:
                if time.time() - start > timeout:
                    raise TimeoutError(f"MySQL at {host}:{port} not available after {timeout}s")
                time.sleep(1)

    def handle(self, *args, **options):
        AWS_DB = {
            "host": "mysql_dev",
            "port": 3306,
            "user": "dev_user",
            "password": "dev_pass",
            "database": "dev_db",
        }

        LOCAL_DB = {
            "host": "mysql_local",
            "port": 3306,
            "user": "local_user",
            "password": "local_pass",
            "database": "local_db",
        }

        DUMP_FILE = "/tmp/dev_dump.sql"

        # --- Step 0: Add dummy data to dev_db ---
        print("📝 Adding dummy data to dev_db ...")
        dummy_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            email VARCHAR(50)
        );
        INSERT INTO users (name, email) VALUES
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com')
        ON DUPLICATE KEY UPDATE name=name;
        """
        subprocess.run(
            f"mysql --protocol=TCP --skip-ssl -h {AWS_DB['host']} -P {AWS_DB['port']} "
            f"-u {AWS_DB['user']} -p{AWS_DB['password']} {AWS_DB['database']} -e \"{dummy_sql}\"",
            shell=True,
            check=True
        )

        # --- Step 1: Dump dev_db ---
        print("🚀 Dumping dev_db ...")
        dump_cmd = (
            f"mysqldump --protocol=TCP --skip-ssl -h {AWS_DB['host']} -P {AWS_DB['port']} "
            f"-u {AWS_DB['user']} -p{AWS_DB['password']} --single-transaction "
            f"--routines --triggers --events {AWS_DB['database']} > {DUMP_FILE}"
        )
        subprocess.run(dump_cmd, shell=True, check=True)

        # --- Step 2: Refresh local_db ---
        print("🧹 Refreshing local_db ...")
        refresh_cmd = (
            f"mysql --protocol=TCP --skip-ssl -h {LOCAL_DB['host']} -P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} -p{LOCAL_DB['password']} "
            f"-e 'DROP DATABASE IF EXISTS {LOCAL_DB['database']}; CREATE DATABASE {LOCAL_DB['database']};'"
        )
        subprocess.run(refresh_cmd, shell=True, check=True)

        # --- Step 3: Wait for local MySQL ---
        print("⏳ Waiting for local MySQL ...")
        self.wait_for_mysql(LOCAL_DB['host'], LOCAL_DB['port'])

        # --- Step 4: Restore to local_db ---
        print("📥 Restoring dev_db dump to local_db ...")
        restore_cmd = (
            f"mysql --protocol=TCP --skip-ssl -h {LOCAL_DB['host']} -P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} -p{LOCAL_DB['password']} {LOCAL_DB['database']} < {DUMP_FILE}"
        )
        subprocess.run(restore_cmd, shell=True, check=True)

        # --- Step 5: Verify ---
        print("✅ Sync completed! Sample data in local_db:")
        verify_cmd = (
            f"mysql --protocol=TCP --skip-ssl -h {LOCAL_DB['host']} -P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} -p{LOCAL_DB['password']} {LOCAL_DB['database']} "
            f"-e 'SELECT * FROM users;'"
        )
        subprocess.run(verify_cmd, shell=True, check=True)
