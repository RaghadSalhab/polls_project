#!/bin/bash
# scripts/import_to_local.sh
DUMP_DIR="./db"   
CONTAINER="mysql_local"   
DB_USER="root"
DB_PASS="root"


echo "🚀 Starting import of SQL dumps into local Docker MySQL..."
echo "🔍 Source directory: $DUMP_DIR"
echo "🐳 Target container: $CONTAINER"
echo

START_TIME=$(date +%s)

echo "🧹 Normalizing dump files (fixing line endings)..."
find "$DUMP_DIR" -name "*.sql" -exec sed -i 's/\r$//' {} \;

for DUMP_FILE in "$DUMP_DIR"/*.sql; do
    [ -e "$DUMP_FILE" ] || { echo "❌ No .sql dump files found."; exit 1; }

    DB_NAME=$(basename "$DUMP_FILE" .sql)
    echo "🧩 Creating database \`$DB_NAME\` inside container $CONTAINER ..."
    docker exec -i "$CONTAINER" mysql -u"$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"

    echo "📥 Importing schema for \`$DB_NAME\` ..."
    start_time=$(date +%s)

    # ✅ Correct way on Windows
    cat "$DUMP_FILE" | docker exec -i "$CONTAINER" mysql -u"$DB_USER" -p"$DB_PASS" "$DB_NAME"

    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "✅ Done importing: $DB_NAME (⏱ ${duration}s)"
done


END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo "🎉 All databases imported successfully!"
echo "⏱ Total import time: $TOTAL_DURATION seconds"
