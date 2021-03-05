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

ACCESS_TOKEN=$(curl -d client_id="$API_CLIENT_ID" -d client_secret="$API_CLIENT_SECRET" -d grant_type=refresh_token -d refresh_token="$API_REFRESH_TOKEN" "https://www.googleapis.com/oauth2/v4/token" | jq -r '.access_token')

curl -X POST -L   \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "metadata={name :'$file_name', parents: ['$API_PARENT_ID']};type=application/json;charset=UTF-8" \
  -F "file=@$file_name;type=application/zip" "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
cd .. || exit 1
rm -rf tmp
exit 0