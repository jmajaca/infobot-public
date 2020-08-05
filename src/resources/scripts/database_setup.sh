#!/bin/bash

docker run --name "$1" -e POSTGRES_PASSWORD="$2" -d postgres
docker exec -it "$1" psql -U postgres
echo create database infobot;