# scripts/sync_rds_to_docker.py
import os
import subprocess
import pymysql
import time

# === إعدادات RDS ===
RDS_HOST = "dev-db.rds.amazonaws.com"
RDS_PORT = 3306
RDS_USER = "dev_user"
RDS_PASS = "dev12345678"

# === إعدادات Docker MySQL ===
DOCKER_IMAGE = "mysql:8"
ROOT_PASS = "root"
LOCAL_PORT_START = 3307  # كل container على port مختلف
DUMP_DIR = "./dumps"

os.makedirs(DUMP_DIR, exist_ok=True)

conn = pymysql.connect(host=RDS_HOST, port=RDS_PORT, user=RDS_USER, password=RDS_PASS)
with conn.cursor() as cursor:
    cursor.execute("SHOW DATABASES;")
    dbs = [row[0] for row in cursor.fetchall() if row[0] not in ('mysql','information_schema','performance_schema')]
conn.close()

print("📦 Databases found on RDS:", dbs)

# --- 2️⃣ عمل schema dump لكل database ---
for db in dbs:
    dump_file = os.path.join(DUMP_DIR, f"{db}.sql")
    print(f"💾 Dumping schema for {db}...")
    dump_cmd = (
        f"mysqldump --protocol=TCP --no-data -h {RDS_HOST} -P {RDS_PORT} "
        f"-u {RDS_USER} -p{RDS_PASS} {db} > {dump_file}"
    )
    subprocess.run(dump_cmd, shell=True, check=True)

# --- 3️⃣ إنشاء containers لكل database ---
for i, db in enumerate(dbs):
    port = LOCAL_PORT_START + i
    container_name = f"mysql_{db}"
    
    # تحقق إذا container موجود
    result = subprocess.run(f"docker ps -a --filter name={container_name} --format '{{{{.Names}}}}'", 
                            shell=True, capture_output=True, text=True)
    if container_name in result.stdout:
        print(f"♻️ Container {container_name} already exists, skipping creation.")
    else:
        print(f"🐳 Creating container {container_name} on port {port}...")
        run_cmd = (
            f"docker run -d --name {container_name} "
            f"-e MYSQL_ROOT_PASSWORD={ROOT_PASS} "
            f"-e MYSQL_DATABASE={db} "
            f"-p {port}:3306 {DOCKER_IMAGE}"
        )
        subprocess.run(run_cmd, shell=True, check=True)
    
    # --- 4️⃣ انتظر MySQL ليشتغل ---
    print(f"⏳ Waiting for {container_name} MySQL to be ready...")
    start = time.time()
    while True:
        try:
            conn = pymysql.connect(host="127.0.0.1", port=port, user="root", password=ROOT_PASS)
            conn.close()
            break
        except Exception:
            if time.time() - start > 30:
                raise TimeoutError(f"MySQL container {container_name} not ready after 30s")
            time.sleep(1)
    
    # --- 5️⃣ Restore schema ---
    dump_file = os.path.join(DUMP_DIR, f"{db}.sql")
    print(f"📥 Restoring schema for {db} into {container_name}...")
    restore_cmd = f"mysql -h 127.0.0.1 -P {port} -uroot -p{ROOT_PASS} {db} < {dump_file}"
    subprocess.run(restore_cmd, shell=True, check=True)

print("✅ All RDS schemas synced to local Docker containers!")
