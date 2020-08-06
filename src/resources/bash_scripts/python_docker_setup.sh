#!/bin/bash

echo Python docker init

cd ../..
docker build --tag infobot-app -f Dockerfile .
docker run --name infobot-app -p 9000:9000 infobot-app