import os
import mysql.connector
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Sync AWS RDS dev DB to local MySQL"

    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Clear local database before syncing'
        )

    def handle(self, *args, **options):
        refresh = options['refresh']

        # --- Dev DB on AWS RDS ---
        DEV_DB = {
            "host": "dev-db.c9y28auwabnd.eu-north-1.rds.amazonaws.com",
            "port": 3306,
            "user": "dev_user",
            "password": "dev12345678",
            "database": "dev_db",
        }

        # --- Local DB ---
        LOCAL_DB = {
            "host": "mysql_local",
            "port": 3306,
            "user": "local_user",
            "password": "local_pass",
            "database": "local_db",
        }

        DUMP_FILE = "dev_dump.sql"

        # --- Step 0: Optionally clear local DB ---
        if refresh:
            self.stdout.write("🧹 Refreshing local database...")
            os.system(f"mysql -h {LOCAL_DB['host']} -P {LOCAL_DB['port']} "
                      f"-u {LOCAL_DB['user']} -p{LOCAL_DB['password']} "
                      f"-e 'DROP DATABASE IF EXISTS {LOCAL_DB['database']}; CREATE DATABASE {LOCAL_DB['database']};'")

        # --- Step 1: Dump DEV DB ---
        self.stdout.write("🚀 Dumping DEV database from AWS RDS ...")
        dump_cmd = (
            f"mysqldump -h {DEV_DB['host']} "
            f"-P {DEV_DB['port']} "
            f"-u {DEV_DB['user']} "
            f"-p{DEV_DB['password']} "
            f"--ssl-mode=DISABLED "
            f"{DEV_DB['database']} > {DUMP_FILE}"
        )
        os.system(dump_cmd)

        # --- Step 2: Restore to LOCAL DB ---
        self.stdout.write("📥 Restoring to LOCAL database ...")
        restore_cmd = (
            f"mysql -h {LOCAL_DB['host']} "
            f"-P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} "
            f"-p{LOCAL_DB['password']} "
            f"{LOCAL_DB['database']} < {DUMP_FILE}"
        )
        os.system(restore_cmd)

        self.stdout.write(self.style.SUCCESS("✅ Database synced successfully!"))
