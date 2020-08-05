#!/bin/bash

apt-get update

echo Installing Git
yes Y | apt install git

echo Installing Docker
yes Y | apt-get remove docker docker-engine docker.io containerd runc
yes Y | apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
if [ ! "$(apt-key fingerprint 0EBFCD88 | grep "9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88")" ]
then
  exit 1
fi
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
apt-get install docker-ce docker-ce-cli containerd.io


#echo Installing ngrok
#wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.tgz
#tar xvf ngrok-stable-linux-amd64.tgz -C /usr/local/bin