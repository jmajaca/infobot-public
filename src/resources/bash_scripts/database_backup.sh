#!/bin/bash

source ./log_func.sh

while IFS='=' read -ra vars
do
  export "${vars[0]}"="${vars[1]}"
done < ../db_backup.cfg

export PGPASSWORD="$DB_PASSWD"
tables=("user" "slack_user" "channel" "course" "author" "notification" "reminder" "pin" "filter" "reaction")

mkdir tmp
cd tmp || exit 1
echo "$(info_log) Connecting to database"
for table in "${tables[@]}"; do
  echo "$(info_log) Getting data from $table table"
  psql --dbname="$DB_NAME" --username="$DB_USERNAME" --host="$DB_HOST" -p "$DB_PORT" -c "COPY (SELECT * FROM $table) TO stdout DELIMITER ',' CSV HEADER" > "${table}".csv
done

echo "$(info_log) Creating zip file with all data"
file_name=data_SNAPSHOT-"$(date +%Y%m%d)".zip
zip "$file_name" *

echo "$(info_log) Getting access token"
ACCESS_TOKEN=$(curl -d client_id="$API_CLIENT_ID" -d client_secret="$API_CLIENT_SECRET" -d grant_type=refresh_token -d refresh_token="$API_REFRESH_TOKEN" "https://www.googleapis.com/oauth2/v4/token" | jq -r '.access_token')

echo "$(info_log) Uploading data to Google Drive"
curl -X POST -L   \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -F "metadata={name :'$file_name', parents: ['$API_PARENT_ID']};type=application/json;charset=UTF-8" \
  -F "file=@$file_name;type=application/zip" "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
echo "$(info_log) Uploaded data to Google Drive"

echo "$(info_log) Checking if number of snapshots is over the limit"
echo "$(info_log) Get list of file IDs"
file_ids=($(curl 'https://www.googleapis.com/drive/v3/files?corpora=user' \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H 'Accept: application/json' | jq -r '.files' | jq -r '.[].id'))

if [ ${#file_ids[@]} -gt 5 ]
then
  echo "$(info_log) Number of snapshots is greater than 5, sending delete request"
  curl -X DELETE "https://www.googleapis.com/drive/v3/files/${file_ids[-1]}" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H 'Accept: application/json'
  echo "$(info_log) Delete request sent"
else
  echo "$(info_log) Number of snapshots is lower or equal to 5, skipping deletion"
fi

echo "$(info_log) Cleaning up"
cd .. || exit 1
rm -rf tmp
exit 0