
#!/bin/bash
# scripts/dump_local_dbs.sh

DOCKER_CONTAINER="mysql_dev"
DB_USER="root"
DB_PASSWORD="root"
OUTPUT_DIR="./db"

mkdir -p "$OUTPUT_DIR"

START_TIME=$(date +%s)

DBS=$(docker exec -i $DOCKER_CONTAINER mysql -u$DB_USER -p$DB_PASSWORD -e "SHOW DATABASES;" \
    | grep -vE 'Database|information_schema|mysql|performance_schema|sys' \
    | grep -E '^dev_db')

for DB_NAME in $DBS; do
    OUTPUT_FILE="$OUTPUT_DIR/${DB_NAME}_dump.sql"
    echo "🧩 Dumping schema from $DB_NAME ..."

    docker exec -i $DOCKER_CONTAINER mysqldump -u$DB_USER -p$DB_PASSWORD --no-data "$DB_NAME" > "$OUTPUT_FILE"

    if [ -f "$OUTPUT_FILE" ]; then
        echo "✅ Schema dump saved to $OUTPUT_FILE"
    else
        echo "❌ Failed to dump schema for $DB_NAME"
    fi
done

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo "🎉 All local dev database schemas dumped successfully!"
echo "⏱ Total time for all dumps: $TOTAL_DURATION seconds"
