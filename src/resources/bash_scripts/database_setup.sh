#!/bin/bash

nohup docker-compose -p test8 -f ../docker-compose.yml up &> ../../log/docker_log.log
