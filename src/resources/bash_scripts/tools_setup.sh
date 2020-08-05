#!/bin/bash

apt-get update

echo Installing Git
yes Y | apt install git

echo Installing Docker
cd /tmp || exit
mkdir docker
cd docker || exit
curl -O https://download.docker.com/linux/debian/dists/stretch/pool/stable/amd64/containerd.io_1.2.6-3_amd64.deb
curl -O https://download.docker.com/linux/debian/dists/stretch/pool/stable/amd64/docker-ce-cli_19.03.9~3-0~debian-stretch_amd64.deb
curl -O https://download.docker.com/linux/debian/dists/stretch/pool/stable/amd64/docker-ce_19.03.9~3-0~debian-stretch_amd64.deb
dpkg -i containerd.io_1.2.6-3_amd64.deb
dpkg -i docker-ce-cli_19.03.9~3-0~debian-stretch_amd64.deb
dpkg -i docker-ce_19.03.9~3-0~debian-stretch_amd64.deb
cd ..
rm -rf docker
docker run hello-world

curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

#echo Installing ngrok
#wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz
#tar xvf ngrok-stable-linux-amd64.tgz -C /usr/local/bin