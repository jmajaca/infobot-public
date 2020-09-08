# Initial setup

> Notice: all scripts bellow (w/o python installation on server) can be run at once with 
> `sudo bash start_application.sh [file_id]`

## Download git project

First step is to clone git project on local device. Before doing that *git* needs
to be installed via command `sudo apt install git`. Cloning project repository is
then easy and can be done with command: `git clone https://github.com/jmajaca/infobot-public.git`.

## Python 3.7 setup for Debian GNU/Linux 9 (stretch)

> Notice: Skip this step if you are not planing to develop application or create hotfixes
> directly on server. Alternative to installing Python directly on the server is to run 
> python application in docker container which
> will be described in one of the following chapters.

To install Python 3.7 and its dependencies as well as packages for infobot-public
project run following command:
`sudo bash python_setup.sh`. Script follows instructions for installing Python
3.7 on Debian 9 Device from [this](https://linuxize.com/post/how-to-install-python-3-7-on-debian-9/)
step by step tutorial.

Script installs these python packages:

* slack
* slackclient
* requests
* bs4
* sqlalchemy
* psycopg2-binary
* flask

## Tools setup

Tools that are required for project to work correctly are:

* git *(already installed)*
* docker
* unzip
* curl

Docker is installed from a package based on [this](https://docs.docker.com/engine/install/debian/)
official tutorial.

Run command `sudo bash tools_setup.sh` to install listed tools.

## Docker containers setup

To initialize database and application docker containers you will need access
to files *config.cfg* and *docker-compose.yml* which both contain sensitive data.
To get access to these two files you will need to contact project maintainer
so that he could potentially give you id of zip file which contains these two
files. You will then need to pass that id as a parameter of bash script call
so that script knows which file to download from Google Drive.
When you have file id run command
`sudo bash containers_setup.sh [file_id]`.

### Database

This part of setup is based on [this](https://phoenixnap.com/kb/deploy-postgresql-on-docker)
and [this](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-debian-9) tutorial. 
For script to work you will need **docker-compose.yaml** 
file in which options are defined. File can be accessed as described earlier.
Command will create two databases: one for production and one for testing. Both databases will be initialized with empty
tables from infobot project. Production database is on default postgres port `5432` while test database is on port
`5431`.

### Application

Docker bash script will install
requirements (as described in first chapter of this file regarding installation of Python)
and start application with exposed port `9000`. 
For script to work you will need **config.cfg** 
file in which options are defined. File can be accessed as described earlier.
Entry method is located in `start.py` file.

## Google Cloud Platform Setup *(Optional)*

### Creating instance

Instance is created with following settings.

|     Setting             |     Value     |
| :------------------ | :-------------------|
| Name | *optional* |
| Region | europe-west3 (Frankfurt) |
| Zone | europe-west3-c |
| Machine Family | General-purpose |
| Machine Series | N1 |
| Machine Type | f1-micro (1 vCPU, 614 MB memory) |
| Boot Disk | Debian GNU/Linux 9 (stretch) |

### Editing instance

#### SSH key

To connect locally to server you need SSH key which can be easily added.
To edit instance click *edit* when on VM instance details page.
In edit mode under section **SSH Keys** click on *Show and edit* which will
open a form for adding or deleting ssh keys.

#### Firewall rules

To expose ports to outside world you will need to create Firewall rules. Follow
[this](https://stackoverflow.com/questions/21065922/how-to-open-a-specific-port-such-as-9090-in-google-compute-engine)
link for more information.
You will want to create rules that expose ports `5432`, `5431` and `9000` to all (IP range: `0.0.0.0/0`).

# Bonus

## Logs

Logs can be found in `src/log` folder. Here is the table of logs found in that file.

|     Log             |     Description     |
| :------------------ | :-------------------|
| docker_db_log.log   | Logs from docker container that contains test and production database |
| docker_app_log.log  | Logs from docker container that contains python application |
| application_log.log | Logs from python application |
| application_trace.log | Trace stack from errors that are logged in `application_log.log` |

## Slack Workspace Description

### Test Workspace

For test workspace url please contact project maintainer.

### Bot permissions

Infobot has following permissions on slack workspace:

|     OAuth Scope     |     Description     |
| :------------------ | :-------------------|
| app_mentions:read   | View messages that directly mention @infobot in conversations that the app is in |
| channels:read      | View basic information about public channels in the workspace |
| chat:write | Send messages as @infobot |
| chat:write.public | Send messages to channels @infobot isn't a member of |
| im:read | View basic information about direct messages that Infobot has been added to |
| im:write | Start direct messages with people |
| pins:read | View pinned content in channels and conversations that Infobot has been added to |
| pins:write | Add and remove pinned messages and files |
| reactions: read | View emoji reactions and their associated content in channels and conversations that Infobot has been added to |
| users:read | View people in the workspace |

## Local init

For program to be able to run locally you will need file **config.cfg** stored on path `src/resources/config.cfg`.
If you don't have config file please contact project maintainer. Next step is to install Python requirements, this
can easily be done with command `pip install -r src/resources/requirements.txt` from project root folder. Project entry 
point is located in `start.py` in project root folder. Application is started by running `start.py`.
By default config application is running on `http://localhost:9000` and is connected to test database on port `5432`.
If config is not default these options can differ.