# Initial setup

> Notice: all scripts bellow can be run at once with `sudo bash complete_setup.sh`

## Python 3.7 setup for Debian GNU/Linux 9 (stretch)

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

## Database setup

This part of setup is based on [this](https://phoenixnap.com/kb/deploy-postgresql-on-docker)
tutorial. To setup database run command `sudo bash database_setup.sh [container_name] [postgres_password]`.
Command will first create empty docker container containing postgres database and
then it will fill database with tables from infobot-public project.


## Slack Test Workspace setup