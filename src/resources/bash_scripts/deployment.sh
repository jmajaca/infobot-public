#!/bin/bash

info_log () {
  echo "---- INFO - [$(date +%d.%m.%Y-%H:%M:%S.%N)] --"
}

echo "$(info_log) Deploy script started"
docker stop infobot-app > /dev/null 2>&1
echo "$(info_log) Stopped infobot-app container"
docker rm infobot-app > /dev/null 2>&1
echo "$(info_log) Removed infobot-app container"
cd ~/git/infobot-public || exit 1
echo "$(info_log) Pulling from git repo"
git pull
docker build --tag infobot-app -f Dockerfile .
echo "$(info_log) Build new docker image finished"
docker run --name infobot-app -p 9000:9000 infobot-app &
echo "$(info_log) Infobot application started"
exit 0