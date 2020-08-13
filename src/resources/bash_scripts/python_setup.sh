#!/bin/bash

echo Installing Python 3.7 process start
apt update
echo Installing libs
apt yes Y | install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl
echo Downloading Python 3.7
curl -O https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tar.xz
echo Download complete
tar -xf Python-3.7.3.tar.xz
echo Checking for dependencies
cd Python-3.7.3 || exit
./configure --enable-optimizations
echo Starting build
make -j 1
echo Installing Python binaries
make altinstall
echo "Python 3.7 installation done"
python3.7 --version
echo "Installing Python 3.7 process done"

yes Y | rm Python-3.7.3.tar.xz

echo Installing Python packages important for infobot-public start
python3.7 -m pip install pip

echo Installing slack package
sudo python3.7 -m pip install slack

echo Installing slackclient package
sudo python3.7 -m pip install slackclient

echo Installing requests package
sudo python3.7 -m pip install requests

echo Installing bs4 package
sudo python3.7 -m pip install bs4

echo Installing psycopg2-binary package
sudo python3.7 -m pip install psycopg2-binary

echo Installing sqlalchemy package
sudo python3.7 -m pip install sqlalchemy

echo Installing flask package
sudo python3.7 -m pip install flask

echo "Installing Python packages important for infobot-public done"

