import mysql.connector

# الاتصال بقاعدة البيانات داخل Docker
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,  # البورت اللي ربطتيه مع الحاوية
    user="dev_user",
    password="dev_pass",
    database="dev_db"
)
cursor = conn.cursor()

num_tables = 100
num_columns = 20

for i in range(1, num_tables + 1):
    table_name = f"table_{i}"
    # توليد الأعمدة
    columns = ["id INT AUTO_INCREMENT PRIMARY KEY"]
    for j in range(1, num_columns):
        columns.append(f"col_{j} VARCHAR(100)")

    columns_sql = ", ".join(columns)
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
    cursor.execute(sql)

conn.commit()
cursor.close()
conn.close()

print("100 tables created successfully!")
