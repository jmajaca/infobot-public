#!/bin/bash

while IFS='=' read -ra vars
do
  export "${vars[0]}"="${vars[1]}"
done < ../db_backup.cfg

export PGPASSWORD="$DB_PASSWD"
tables=("user" "slack_user" "channel" "course" "author" "notification" "reminder" "pin" "filter" "reaction")

mkdir tmp
cd tmp || exit 1
for table in "${tables[@]}"; do
  psql --dbname="$DB_NAME" --username="$DB_USERNAME" --host="$DB_HOST" -p "$DB_PORT" -c "COPY (SELECT * FROM $table) TO stdout DELIMITER ',' CSV HEADER" > "${table}".csv
done
file_name=data_SNAPSHOT-"$(date +%Y%m%d)".zip
zip "$file_name" *
curl -X POST -L   \
  -H "Authorization: Bearer $API_TOKEN" \
  -F "metadata={name :'$file_name', parents: ['$API_PARENT_ID']};type=application/json;charset=UTF-8" \
  -F "file=@$file_name;type=application/zip"     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
cd .. || exit 1
rm -rf tmp
exit 0