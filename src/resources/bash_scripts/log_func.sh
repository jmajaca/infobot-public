#!/bin/bash

log () {
  echo "---- $1 -- [$(date +%d.%m.%Y-%H:%M:%S.%N)] --"
}

info_log() {
  log "INFO"
}

error_log() {
  log "ERROR"
}

warning_log() {
  log "WARNING"
}