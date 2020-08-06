# Initial server setup

> Notice: all scripts bellow can be run at once with `sudo bash complete_setup.sh`

## Python 3.7 setup for Debian GNU/Linux 9 (stretch)

> Notice: Skip this step if you are not planing to develop application or create hotfixes
> directly on server. Alternative is to run python application in docker container which
> will be described in one of the following chapters.

To install Python 3.7 and its dependencies as weel as packages for infobot-public
project run following command:
`sudo bash python_setup.sh`. Script follows instructions for installing Python
3.7 on Debian 9 Device from [this](https://linuxize.com/post/how-to-install-python-3-7-on-debian-9/)
step by step tutorial.

Script installs these python packages:

* slack
* slackclient
* requests
* bs4

## Tools setup

Tools that are required for project to work correctly are:

* git
* docker

Docker is installed from a package based on [this](https://docs.docker.com/engine/install/debian/)
official tutorial.

Run command `sudo bash tools_setup.sh` to install listed tools.

## Docker database setup

This part of setup is based on [this](https://phoenixnap.com/kb/deploy-postgresql-on-docker)
and [this](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-debian-9) tutorial. 
To setup database run command `sudo bash database_setup.sh`. For script to work you will need **docker-compose.yaml** 
file in which options are defined. File can be accessed via API from `**TODO** api_url`.
Command will create two databases: one for production and one for testing. Both databases will be initialized with empty
tables from infobot project. Production database is on default postgres port `5432` while test database is on port
`5431`.

## Docker application setup
