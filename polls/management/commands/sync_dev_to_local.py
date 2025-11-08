import os
from django.core.management.base import BaseCommand
import mysql.connector

class Command(BaseCommand):
    help = "Sync DEV database to LOCAL database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Refresh LOCAL database before restoring"
        )

    def handle(self, *args, **options):
        DEV_DB = {
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

        DUMP_FILE = "dev_dump.sql"

        self.stdout.write("🚀 Preparing DEV database with dummy data...")

        # --- Connect to DEV and ensure dummy tables exist ---
        dev_conn = mysql.connector.connect(
            host=DEV_DB['host'],
            port=DEV_DB['port'],
            user=DEV_DB['user'],
            password=DEV_DB['password'],
            database=DEV_DB['database']
        )
        cursor = dev_conn.cursor()

        tables = {
            "users": [
                ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
                ("name", "VARCHAR(50)"),
                ("email", "VARCHAR(50)")
            ],
            "products": [
                ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
                ("name", "VARCHAR(50)"),
                ("price", "DECIMAL(10,2)")
            ],
            "orders": [
                ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
                ("user_id", "INT"),
                ("product_id", "INT"),
                ("quantity", "INT")
            ]
        }

        for table_name, columns in tables.items():
            cols_def = ", ".join([f"{col[0]} {col[1]}" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_def});")

        # Insert dummy data if empty
        cursor.execute("SELECT COUNT(*) FROM users;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO users (name, email) VALUES (%s, %s)", [
                ("Alice", "alice@example.com"),
                ("Bob", "bob@example.com"),
                ("Charlie", "charlie@example.com")
            ])
            dev_conn.commit()

        cursor.execute("SELECT COUNT(*) FROM products;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s)", [
                ("Laptop", 1200.50),
                ("Phone", 699.99),
                ("Tablet", 399.99)
            ])
            dev_conn.commit()

        cursor.execute("SELECT COUNT(*) FROM orders;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", [
                (1, 2, 1),
                (2, 1, 2),
                (3, 3, 1)
            ])
            dev_conn.commit()

        cursor.close()
        dev_conn.close()
        self.stdout.write("✅ DEV database ready!")

        # --- Optional: refresh LOCAL DB ---
        if options['refresh']:
            self.stdout.write("♻️  Refreshing LOCAL database...")
            for table_name in tables.keys():
                os.system(f"mysql -h {LOCAL_DB['host']} -P {LOCAL_DB['port']} -u {LOCAL_DB['user']} -p{LOCAL_DB['password']} -e 'DROP TABLE IF EXISTS {table_name};' {LOCAL_DB['database']}")
            self.stdout.write("✅ LOCAL database cleared!")

        # --- Dump DEV DB ---
        self.stdout.write("🚀 Dumping DEV database ...")
        dump_cmd = (
            f"mysqldump -h {DEV_DB['host']} "
            f"-P {DEV_DB['port']} "
            f"-u {DEV_DB['user']} "
            f"-p{DEV_DB['password']} "
            f"--ssl=0 "
            f"--no-tablespaces "
            f"{DEV_DB['database']} > {DUMP_FILE}"
        )
        os.system(dump_cmd)

        # --- Restore to LOCAL DB ---
        self.stdout.write("📥 Restoring to LOCAL database ...")
        restore_cmd = (
            f"mysql -h {LOCAL_DB['host']} "
            f"-P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} "
            f"-p{LOCAL_DB['password']} "
            f"--ssl=0 "
            f"{LOCAL_DB['database']} < {DUMP_FILE}"
        )
        os.system(restore_cmd)

        self.stdout.write("✅ Database synced successfully!")
