# import mysql.connector

# # الاتصال بقاعدة البيانات داخل Docker
# conn = mysql.connector.connect(
#     host="127.0.0.1",
#     port=3307,  # البورت اللي ربطتيه مع الحاوية
#     user="dev_user",
#     password="dev_pass",
#     database="dev_db"
# )
# cursor = conn.cursor()

# num_tables = 100
# num_columns = 20

# for i in range(1, num_tables + 1):
#     table_name = f"table_{i}"
#     # توليد الأعمدة
#     columns = ["id INT AUTO_INCREMENT PRIMARY KEY"]
#     for j in range(1, num_columns):
#         columns.append(f"col_{j} VARCHAR(100)")

#     columns_sql = ", ".join(columns)
#     sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
#     cursor.execute(sql)

# conn.commit()
# cursor.close()
# conn.close()

# print("100 tables created successfully!")
import mysql.connector

# اتصال بـ MySQL داخل Docker
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,  
    user="dev_user",
    password="dev_pass"
)
cursor = conn.cursor()

num_databases = 20
num_tables = 30    
num_columns = 15     

for db_index in range(1, num_databases + 1):
    db_name = f"dev_db_{db_index}"
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    print(f"✅ Database created: {db_name}")

    cursor.execute(f"USE {db_name};")

    for table_index in range(1, num_tables + 1):
        table_name = f"table_{table_index}"
        columns = ["id INT AUTO_INCREMENT PRIMARY KEY"]
        for col_index in range(1, num_columns):
            columns.append(f"col_{col_index} VARCHAR(100)")

        columns_sql = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        cursor.execute(sql)

    print(f"   ✅ {num_tables} tables created in {db_name}")

conn.commit()
cursor.close()
conn.close()

print(f"🎉 {num_databases} databases with {num_tables} tables each created successfully!")
