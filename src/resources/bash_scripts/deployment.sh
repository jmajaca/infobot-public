#!/bin/bash

docker stop infobot-app
docker rm infobot-app
cd ~/git/infobot-public || exit 1
git pull
docker build --tag infobot-app f Dockerfile .
docker run --name infobot-app -p 9000:9000 infobot-app | exit 0