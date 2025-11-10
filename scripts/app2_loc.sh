#!/bin/bash
# scripts/import_to_local.sh

DUMP_DIR="./db"
CONTAINER="mysql_local"

SECONDS=0 

for f in "$DUMP_DIR"/*_dump.sql; do
    sed -i 's/\r$//' "$f"
done

for DUMP_FILE in "$DUMP_DIR"/*_dump.sql; do
    DB_NAME="$(basename "$DUMP_FILE" | sed 's/_dump\.sql$//')"

    echo "🧩 Creating database \`$DB_NAME\` in container $CONTAINER ..."

    docker exec -i "$CONTAINER" mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"

    echo "📥 Importing schema & data for \`$DB_NAME\` ..."
    docker exec -i "$CONTAINER" sh -c "mysql -uroot -proot \`$DB_NAME\`" < "$DUMP_FILE"

    echo "✅ Done importing: $DB_NAME"
done

duration=$SECONDS
echo "⏱ Total import time: $duration seconds"
