#!/bin/bash

# 🌐 Dump schema
echo "🌐 Dumping schema from dev DB..."
SECONDS=0
./scripts/dump_schema.sh
dump_time=$SECONDS
echo "⏱ Dump completed in $dump_time seconds"

# 💾 Apply schema
echo "💾 Applying schema to local DB..."
SECONDS=0
docker exec -i mysql_local mysql -u root -proot local_db < db/schema_dump.sql
apply_time=$SECONDS
echo "⏱ Apply completed in $apply_time seconds"

echo "✅ Local DB schema synced successfully!"
