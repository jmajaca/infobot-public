#!/bin/bash

echo Python docker init

cd  "$(dirname "$(realpath "$0")")" || exit 1
cd ../../.. || exit 1
docker build --tag infobot-app -f Dockerfile .
docker run --name infobot-app -p 9000:9000 infobot-app
