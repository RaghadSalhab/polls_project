#!/bin/bash
DOCKER_CONTAINER="mysql_dev"
DB_USER="dev_user"
DB_PASSWORD="dev_pass"
OUTPUT_DIR="./db"
LIST_FILE="./discovered_microservices.txt"

mkdir -p "$OUTPUT_DIR"

CLEAN_FILE="$(mktemp)"
tr -d '\r' < "$LIST_FILE" > "$CLEAN_FILE"

mapfile -t MS_ARRAY < "$CLEAN_FILE"

echo "🚀 Dumping databases for discovered subscriptions..."
START_TIME=$(date +%s)

echo "Discovered microservices:"
for MS_NAME in "${MS_ARRAY[@]}"; do
    echo "$MS_NAME"
done

for MS_NAME in "${MS_ARRAY[@]}"; do
    DB_NAME="${MS_NAME}_db"
    OUTPUT_FILE="$OUTPUT_DIR/${DB_NAME}_dump.sql"

    echo "🧩 Dumping $DB_NAME ..."
    docker exec -i "$DOCKER_CONTAINER" mysqldump -u"$DB_USER" -p"$DB_PASSWORD" --databases "$DB_NAME" > "$OUTPUT_FILE"

    if [ -s "$OUTPUT_FILE" ]; then
        echo "✅ Dump saved: $OUTPUT_FILE"
    else
        echo "⚠️ Failed or empty dump for $DB_NAME"
    fi
done

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

rm "$CLEAN_FILE"

echo "🎉 All subscription-based DBs dumped successfully!"
echo "📦 Output: $OUTPUT_DIR"
echo "⏱ Duration: $DURATION seconds"
