# wait_for_db.py
import os
import time
import psycopg2
from psycopg2 import OperationalError

db_host = os.getenv("DATABASE_HOST", "db")
db_port = os.getenv("DATABASE_PORT", 5432)
db_name = os.getenv("DATABASE_NAME", "polls_db")
db_user = os.getenv("DATABASE_USER", "postgres")
db_password = os.getenv("DATABASE_PASSWORD", "1234")

while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        conn.close()
        print("✅ Database is ready!")
        break
    except OperationalError:
        print("⏳ Waiting for database...")
        time.sleep(2)
