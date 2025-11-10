#!/usr/bin/env python3
import mysql.connector

# ======================
# DATABASE CONNECTION (LOCAL DOCKER)
# ======================
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,           
    user="root",        
    password="root"      
)
cursor = conn.cursor()

# ======================
# DATABASES TO CREATE
# ======================
databases = ["shared", "ms1_db", "ms2_db"]

num_tables = 100       
num_columns = 10      

# ======================
# CREATION LOGIC
# ======================
for db_name in databases:
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    print(f"✅ Database created: {db_name}")
    cursor.execute(f"USE {db_name};")

    for table_index in range(1, num_tables + 1):
        table_name = f"table_{table_index}"
        columns = ["id INT AUTO_INCREMENT PRIMARY KEY"]
        for col_index in range(1, num_columns + 1):
            columns.append(f"col_{col_index} VARCHAR(100)")
        columns_sql = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        cursor.execute(sql)

    print(f"   ✅ {num_tables} tables created in {db_name}")

# ======================
# CLEANUP
# ======================
conn.commit()
cursor.close()
conn.close()

print("\n🎉 All Docker databases created successfully with schema structure!")
