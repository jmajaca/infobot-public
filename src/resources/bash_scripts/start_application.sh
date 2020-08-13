#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
fi

cd  "$(dirname "$(realpath "$0")")" || exit 1
bash tools_setup.sh
bash containers_setup.sh "$1"