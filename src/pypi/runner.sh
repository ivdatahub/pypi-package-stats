SQL_DIR="src/pypi"

for sql_file in "$SQL_DIR"/*.sql; do
  echo "Executing:  $sql_file"
  bq query --use_legacy_sql=false < "$sql_file"
done
