#!/bin/bash
#  scripts/dump_schema.sh
# Configuration
DB_CONTAINER="mysql_dev"
DB_NAME="dev_db"
DB_USER="root"
DB_PASSWORD="root"
OUTPUT_FILE="./db/schema_dump.sql"


echo "🧩 Dumping schema from $DB_NAME ..."

# Start timer
SECONDS=0

# Dump schema
docker exec $DB_CONTAINER \
  sh -c "mysqldump -u$DB_USER -p$DB_PASSWORD --no-data $DB_NAME" > $OUTPUT_FILE

# Calculate elapsed time
duration=$SECONDS

echo "✅ Schema dump saved to $OUTPUT_FILE"
echo "⏱ Operation took $duration seconds"
