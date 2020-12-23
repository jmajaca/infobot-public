#!/bin/bash

cd  "$(dirname "$(realpath "$0")")" || exit 1

mkdir ../../log
touch ../../log/docker_db_log.log
touch ../../log/docker_app_log.log
touch ../../log/application_log.log
touch ../../log/application_trace.log

echo Downloading configuration files

wget -O infobot-public.zip "https://drive.google.com/uc?export=download&id=$1"
unzip infobot-public.zip
rm infobot-public.zip
cp infobot-public/config.cfg ..
cp infobot-public/docker-compose.yml ..
rm -rf infobot-public

echo Database container init

nohup docker-compose -p infobot -f ../docker-compose.yml up &> ../../log/docker_db_log.log &

echo Application container init

cd  "$(dirname "$(realpath "$0")")" || exit 1
cd ../../.. || exit 1
docker build --tag infobot-app -f Dockerfile .
nohup docker run --name infobot-app -p 9000:9000 infobot-app &> src/log/docker_app_log.log &
