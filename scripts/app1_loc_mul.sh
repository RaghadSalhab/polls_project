#!/bin/bash
# scripts/import_to_local_parallel_with_time.sh
# Usage: bash import_to_local_parallel_with_time.sh

# ==============================
# CONFIGURATION
# ==============================
DUMP_DIR="./db"          
CONTAINER="mysql_local"   
MAX_JOBS=8                

# ==============================
# START TIMER
# ==============================
START_TIME=$(date +%s)

echo "🚀 Starting parallel database import..."

# ==============================
# FUNCTION: Import single DB
# ==============================
import_db() {
    local DUMP_FILE=$1
    local DB_NAME=$(basename "$DUMP_FILE" | sed 's/_dump.sql//')
    
    echo "🧩 Creating database $DB_NAME..."
    docker exec -i "$CONTAINER" mysql -uroot -proot -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"

    echo "🧩 Importing schema for $DB_NAME..."
    docker exec -i "$CONTAINER" mysql -uroot -proot "$DB_NAME" < "$DUMP_FILE"

    echo "✅ Done $DB_NAME"
}

# Export function & variables for GNU parallel
export -f import_db
export CONTAINER DUMP_DIR

# ==============================
# PARALLEL EXECUTION
# ==============================
if command -v parallel &> /dev/null; then
    find "$DUMP_DIR" -name "*_dump.sql" | parallel -j $MAX_JOBS import_db {}
else
    echo "⚠️ GNU parallel not found. Running sequentially..."
    for DUMP_FILE in "$DUMP_DIR"/*_dump.sql; do
        import_db "$DUMP_FILE"
    done
fi

# ==============================
# END TIMER
# ==============================
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

echo "⏱ Total import time: $ELAPSED seconds (${MINUTES} min ${SECONDS} sec)"
echo "🎉 All databases imported successfully!"
