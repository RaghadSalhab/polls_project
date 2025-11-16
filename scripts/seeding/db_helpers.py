# db_helpers.py
import mysql.connector

def connect_db(CONFIG, db_name):
    conn = mysql.connector.connect(
        host=CONFIG["host"],
        port=CONFIG["port"],
        user=CONFIG["user"],
        password=CONFIG["password"],
        database=db_name
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def get_tables(cursor, db_name):
    cursor.execute("SHOW TABLES;")
    return [row[f"Tables_in_{db_name}"] for row in cursor.fetchall()]

def get_foreign_keys(cursor, db_name):
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
    """, (db_name,))
    return cursor.fetchall()

def get_columns(cursor, db_name, table):
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s
    """, (db_name, table))
    return cursor.fetchall()

def get_existing_ids(cursor, table, col="id", fk_cache=None):
    """Return existing IDs for a table column (used for foreign keys)."""
    fk_cache = fk_cache if fk_cache is not None else {}
    key = f"{table}.{col}"
    if key in fk_cache:
        return fk_cache[key]

    try:
        cursor.execute(f"SELECT {col} FROM `{table}`;")
        ids = [r[col] for r in cursor.fetchall()]
        fk_cache[key] = ids
        return ids
    except:
        fk_cache[key] = []
        return []

def db_exists(CONFIG, db_name):
    try:
        conn, cursor = connect_db(CONFIG, db_name)
        cursor.close()
        conn.close()
        return True
    except:
        return False

def table_exists(cursor, db_name, table):
    cursor.execute("SHOW TABLES;")
    tables = [list(row.values())[0] for row in cursor.fetchall()]
    return table in tables

def get_unique_columns(cursor, table):
    cursor.execute("""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME=%s AND (COLUMN_KEY='UNI' OR COLUMN_KEY='PRI')
    """, (table,))
    return [row['COLUMN_NAME'] for row in cursor.fetchall()]
