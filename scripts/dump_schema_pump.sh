#!/bin/bash
#  scripts/dump_schema_pump.sh
# Configuration
DB_CONTAINER="mysql_dev"
DB_NAME="dev_db"
DB_USER="root"
DB_PASSWORD="root"
OUTPUT_FILE="./db/schema_dump.sql"

echo "🧩 Dumping schema from $DB_NAME using mysqlpump ..."

# Start timer
SECONDS=0

# Dump schema only using mysqlpump
docker exec $DB_CONTAINER \
  sh -c "mysqlpump -u$DB_USER -p$DB_PASSWORD $DB_NAME --exclude-tables-data='*' --add-drop-database --result-file=/tmp/schema_dump.sql"

# Copy file from container to host
docker cp $DB_CONTAINER:/tmp/schema_dump.sql $OUTPUT_FILE

# Calculate elapsed time
duration=$SECONDS

echo "✅ Schema dump saved to $OUTPUT_FILE"
echo "⏱ Operation took $duration seconds"
