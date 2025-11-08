
# # sync_mysql_dev_to_local.py
# import os

# DEV_DB = {
#     "host": "mysql_dev",
#     "port": 3306,
#     "user": "dev_user",
#     "password": "dev_pass",
#     "database": "dev_db",
# }

# LOCAL_DB = {
#     "host": "mysql_local",
#     "port": 3306,
#     "user": "local_user",
#     "password": "local_pass",
#     "database": "local_db",
# }

# DUMP_FILE = "dev_dump.sql"

# print("🚀 Dumping DEV database ...")
# dump_cmd = (
#     f"mysqldump -h {DEV_DB['host']} "
#     f"-P {DEV_DB['port']} "
#     f"-u {DEV_DB['user']} "
#     f"-p{DEV_DB['password']} "
#     f"--ssl=0 "
#     f"--no-tablespaces "
#     f"{DEV_DB['database']} > {DUMP_FILE}"
# )
# os.system(dump_cmd)

# print("📥 Restoring to LOCAL database ...")
# restore_cmd = (
#     f"mysql -h {LOCAL_DB['host']} "
#     f"-P {LOCAL_DB['port']} "
#     f"-u {LOCAL_DB['user']} "
#     f"-p{LOCAL_DB['password']} "
#     f"--ssl=0 "
#     f"{LOCAL_DB['database']} < {DUMP_FILE}"
# )
# os.system(restore_cmd)

# print("✅ Database synced successfully!")


# # sync_mysql_dev_to_local.py
# import os
# import mysql.connector

# DEV_DB = {
#     "host": "mysql_dev",
#     "port": 3306,
#     "user": "dev_user",
#     "password": "dev_pass",
#     "database": "dev_db",
# }

# LOCAL_DB = {
#     "host": "mysql_local",
#     "port": 3306,
#     "user": "local_user",
#     "password": "local_pass",
#     "database": "local_db",
# }

# DUMP_FILE = "dev_dump.sql"

# # --- Step 0: Connect to DEV and create dummy tables if not exist ---
# dev_conn = mysql.connector.connect(
#     host=DEV_DB['host'],
#     port=DEV_DB['port'],
#     user=DEV_DB['user'],
#     password=DEV_DB['password'],
#     database=DEV_DB['database']
# )
# cursor = dev_conn.cursor()

# # Example tables and dummy data
# tables = {
#     "users": [
#         ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
#         ("name", "VARCHAR(50)"),
#         ("email", "VARCHAR(50)")
#     ],
#     "products": [
#         ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
#         ("name", "VARCHAR(50)"),
#         ("price", "DECIMAL(10,2)")
#     ],
#     "orders": [
#         ("id", "INT PRIMARY KEY AUTO_INCREMENT"),
#         ("user_id", "INT"),
#         ("product_id", "INT"),
#         ("quantity", "INT")
#     ]
# }


# # Create tables if not exist
# for table_name, columns in tables.items():
#     cols_def = ", ".join([f"{col[0]} {col[1]}" for col in columns])
#     cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_def});")

# # Insert dummy data if empty
# cursor.execute("SELECT COUNT(*) FROM users;")
# if cursor.fetchone()[0] == 0:
#     cursor.executemany("INSERT INTO users (name, email) VALUES (%s, %s)", [
#         ("Alice", "alice@example.com"),
#         ("Bob", "bob@example.com"),
#         ("Charlie", "charlie@example.com")
#     ])
#     dev_conn.commit()

# cursor.execute("SELECT COUNT(*) FROM products;")
# if cursor.fetchone()[0] == 0:
#     cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s)", [
#         ("Laptop", 1200.50),
#         ("Phone", 699.99),
#         ("Tablet", 399.99)
#     ])
#     dev_conn.commit()

# cursor.execute("SELECT COUNT(*) FROM orders;")
# if cursor.fetchone()[0] == 0:
#     cursor.executemany("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", [
#         (1, 2, 1),
#         (2, 1, 2),
#         (3, 3, 1)
#     ])
#     dev_conn.commit()

# cursor.close()
# dev_conn.close()

# print("🚀 DEV database prepared with dummy data!")

# # --- Step 1: Dump DEV database ---
# print("🚀 Dumping DEV database ...")
# dump_cmd = (
#     f"mysqldump -h {DEV_DB['host']} "
#     f"-P {DEV_DB['port']} "
#     f"-u {DEV_DB['user']} "
#     f"-p{DEV_DB['password']} "
#     f"--ssl=0 "
#     f"--no-tablespaces "
#     f"{DEV_DB['database']} > {DUMP_FILE}"
# )
# os.system(dump_cmd)

# # --- Step 2: Restore to LOCAL database ---
# print("📥 Restoring to LOCAL database ...")
# restore_cmd = (
#     f"mysql -h {LOCAL_DB['host']} "
#     f"-P {LOCAL_DB['port']} "
#     f"-u {LOCAL_DB['user']} "
#     f"-p{LOCAL_DB['password']} "
#     f"--ssl=0 "
#     f"{LOCAL_DB['database']} < {DUMP_FILE}"
# )
# os.system(restore_cmd)

# print("✅ Database synced successfully!")
import os
import time
import socket
from django.core.management.base import BaseCommand
import mysql.connector

class Command(BaseCommand):
    help = "Sync AWS dev_db to local DB with optional refresh"

    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh',
            action='store_true',
            help='Clear local DB before syncing',
        )

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
        refresh = options['refresh']

        AWS_DB = {
            "host": "dev-db.c9y28auwabnd.eu-north-1.rds.amazonaws.com",
            "port": 3306,
            "user": "dev_user",
            "password": "dev12345678",
            "database": "dev_db",
        }

        LOCAL_DB = {
            "host": "mysql_local",
            "port": 3306,
            "user": "local_user",
            "password": "local_pass",
            "database": "local_db",
        }

        DUMP_FILE = "aws_dev_dump.sql"

        # --- Step 0: Connect to AWS DB and create dummy tables ---
        self.stdout.write("🚀 Connecting to AWS dev_db ...")
        aws_conn = mysql.connector.connect(
            **AWS_DB,
            ssl_disabled=True  # تجاوز SSL عند الاتصال من كود بايثون
        )
        cursor = aws_conn.cursor()

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
            aws_conn.commit()

        cursor.execute("SELECT COUNT(*) FROM products;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO products (name, price) VALUES (%s, %s)", [
                ("Laptop", 1200.50),
                ("Phone", 699.99),
                ("Tablet", 399.99)
            ])
            aws_conn.commit()

        cursor.execute("SELECT COUNT(*) FROM orders;")
        if cursor.fetchone()[0] == 0:
            cursor.executemany("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", [
                (1, 2, 1),
                (2, 1, 2),
                (3, 3, 1)
            ])
            aws_conn.commit()

        cursor.close()
        aws_conn.close()
        self.stdout.write(self.style.SUCCESS("🚀 AWS dev_db prepared with dummy data!"))

        # --- Step 1: Dump AWS DB (disable SSL properly) ---
        self.stdout.write("🚀 Dumping AWS dev_db ...")
        dump_cmd = (
            f"mysqldump --protocol=TCP --ssl-mode=DISABLED "
            f"-h {AWS_DB['host']} "
            f"-P {AWS_DB['port']} "
            f"-u {AWS_DB['user']} "
            f"-p{AWS_DB['password']} "
            f"{AWS_DB['database']} > {DUMP_FILE}"
        )
        os.system(dump_cmd)

        # --- Step 2: Optionally refresh local DB ---
        if refresh:
            self.stdout.write("🧹 Refreshing local DB ...")
            refresh_cmd = (
                f"mysql --protocol=TCP --ssl-mode=DISABLED "
                f"-h {LOCAL_DB['host']} "
                f"-P {LOCAL_DB['port']} "
                f"-u {LOCAL_DB['user']} "
                f"-p{LOCAL_DB['password']} "
                f"-e 'DROP DATABASE IF EXISTS {LOCAL_DB['database']}; CREATE DATABASE {LOCAL_DB['database']};'"
            )
            os.system(refresh_cmd)

        # --- Step 3: Wait for LOCAL MySQL before restore ---
        self.stdout.write("⏳ Waiting for local MySQL to be ready ...")
        self.wait_for_mysql(LOCAL_DB['host'], LOCAL_DB['port'])

        # --- Step 4: Restore to LOCAL DB ---
        self.stdout.write("📥 Restoring to LOCAL DB ...")
        restore_cmd = (
            f"mysql --protocol=TCP --ssl-mode=DISABLED "
            f"-h {LOCAL_DB['host']} "
            f"-P {LOCAL_DB['port']} "
            f"-u {LOCAL_DB['user']} "
            f"-p{LOCAL_DB['password']} "
            f"{LOCAL_DB['database']} < {DUMP_FILE}"
        )
        os.system(restore_cmd)

        self.stdout.write(self.style.SUCCESS("✅ AWS dev_db synced to local DB successfully!"))
