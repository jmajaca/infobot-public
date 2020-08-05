#!/bin/bash

if [ ! -f ../../log/docker_log.log ]; then
        if [ ! -d ../../log ]; then
                mkdir ../../log
        fi
        touch ../../log/docker_log.log
fi

nohup docker-compose -p infobot -f ../docker-compose.yml up &> ../../log/docker_log.log &
