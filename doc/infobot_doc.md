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
* flask_wtf

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

<details>

<summary>Click for more information</summary>

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

</details>

## Local init

For program to be able to run locally you will need file **config.cfg** stored on path `src/resources/config.cfg`.
If you don't have config file please contact project maintainer. Next step is to install Python requirements, this
can easily be done with command `pip install -r src/resources/requirements.txt` from project root folder. Project entry 
point is located in `start.py` in project root folder. 
The last thing is to create log files which can be done from the project root folder with command
`mkdir src/log touch src/log/{application_log.log,application_trace.log}`.
Application is started by running `start.py`.
By default config application is running on `http://localhost:9000` and is connected to test database on port `5431`.
If config is not default these options can differ.

## Database info

<details>

<summary>Click for more information</summary>

### Diagram

![Alt text](images/dbdiagram.png?raw=true "Database diagram")

### Description

#### Notification

This table contains all relevant data of notification that is beaning scrapped.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated notification identification |
| title | VARCHAR | title of the notification |
| author | INTEGER | foreign key that is unique identification of the notification author |
| site | INTEGER | foreign key that is unique identification of the notification course |
| publish_date | TIMESTAMP | date and time when the notification was published |
| text | VARCHAR | text of the notification parsed for the Slack messaging |
| link | VARCHAR | link to the original notification that was scrapped |

#### Reminder

This table represents autogenerated reminders from scrapped notifications.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated reminder identification |
| text | VARCHAR | text of the reminder (one notification paragraph) parsed for the Slack messaging |
| end_date | TIMESTAMP | date and time when the event in the reminder is meant to happen |
| timer | INTERVAL | time before `end_date` when reminder is meant to be sent as a Slack message |
| posted | BOOLEAN | flag that tells if reminder has already been sent |

#### Channel

This table represents Slack channels from selected Slack Workspace.

| name | type | description |
| :--- | :--- | :---------- |
| id | VARCHAR | unique channel identification generated by Slack |
| tag | VARCHAR | channel tag |
| creator_id | VARCHAR | foreign key that is unique identification of Slack user who created the channel |
| created | TIMESTAMP | date and time when the channel was created |

#### Course

This table represents a faculty course.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated course identification |
| name | VARCHAR | course name |
| channel_tag | VARCHAR | foreign key that connects course and channel via channel tag |
| url | VARCHAR | course url on the internet |
| watch | BOOLEAN | flag that tells if course is on the watchlist, if course is on the watchlist the scraper is going to scrape notifications for the course via url |

#### Author

This table represent an author of the notification that was scrapped.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated author identification |
| first_name | VARCHAR | author's first name |
| last_name | VARCHAR | author's last name |

#### Pin

This table represents a message pin from the Slack Workspace.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated pin identification |
| creation_date | TIMESTAMP | date and time when the pin was created |
| timer | INTERVAL | time for how long the message is going to be pinned |
| notification | INTEGER | foreign key of the notification that was pinned |
| timestamp | FLOAT | unique message identification represented as [timestamp](https://api.slack.com/messaging/retrieving#individual_messages)
| done | BOOLEAN | flag that tells if pin is done, if pin is done then it is unpinned |

#### Slack User

This table represents a Slack user from the Slack Workspace.

| name | type | description |
| :--- | :--- | :---------- |
| id | VARCHAR | unique user identification generated by Slack |
| name | VARCHAR | slack username generated from user's e-mail |

#### Reaction

This table represents a reaction from the Slack Workspace.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated reaction identification |
| name | VARCHAR | reactions name in the Slack Workspace |
| timestamp | FLOAT | unique message identification represented as [timestamp](https://api.slack.com/messaging/retrieving#individual_messages) on which the reaction was given
| sender | VARCHAR | foreign key that is unique identification of Slack user who gave the reaction |
| receiver | VARCHAR | foreign key that is unique identification of Slack user who received the reaction |

#### User

This table represent a user that can log in on the web application. 
This table is not to be confused with *Slack User* table.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated user identification |
| name | VARCHAR | username |
| password | VARCHAR | hashed user's password |

#### Filter

> Notice: this table is yet to be clearly defined, as of now it is not used in the application

This table represents filters on scrapping notifications.

| name | type | description |
| :--- | :--- | :---------- |
| id | SERIAL | unique autogenerated filter identification |
| ban_title | VARCHAR | title regex that if matched means that notification is not scrapped |

</details>

## Web application views

<details>

<summary>Click for more information</summary>

### Navigation bar

![Alt text](images/navigation_bar.png?raw=true "Navigation bar")

Navigation bar has 6 main buttons: **Home**, **Courses**, **Reminders**, **Reactions**, **Scan** and button containing username of
logged in user. Click on the application icon or **Infobot** text next to is going to redirect user to **Home** page.
Also there is scrapper status on the right side of navigation bar near logged in user. Scrapper status is changed dynamically.
Scrapper can have 4 statuses (all in different color): *Off*, *Scrapping*, *Sleeping*, *Error*. Click on the status is redirecting user to **Home** page.
Buttons **Home**, **Courses**, **Reminders** and **Reactions** are redirecting to corresponding pages. Button **Scan** opens a
dropdown that has following options: **Scan for users**, **Scan for channels**, **Scan for reactions** and **Complete scan**
which starts all other scans by one click. All scans are done on the Slack Workspace. For scanning users and channels class
`Scanner` is used and for reactions scan class `ReactionManager` is used. When clicked on a scan spinner is appearing for the duration
of scanning. If scan finished without errors check mark will replace spinner, if that is not the case error icon will appear.

![Alt text](images/scan.png?raw=true "Scan")

On the far right there is username of logged in user along with user icon. By clicking on the username dropdown appears that has following options:
*Settings* and *Logout*. By clicking on *Settings* user open it's profile settings where he can change his user settings.
Click on the *Logout* is going to logout user and redirect him to login page.

![Alt text](images/user_actions.png?raw=true "User actions")

Navigation bar html code is located in `base.html` as it is JavaScript code for navigation bar actions. Backend logic is located
in `nav_bar_view.py`. Scraper progress is stored in *localStorage* in `base.html` from endpoint
`progress` in `base_view.py`. Scraper status card gets its value from that stored value in *localStorage*.

### Home

On home page are the most important things about Infobot - it's scrapping status and log entries.

![Alt text](images/home.png?raw=true "Home")

Progress bar tells user what is the progress of scrapping and description of current scraping phase.
Progress bar is getting information from the same place as scraping status in the navigation bar.
There are two states of progress bar: running (blue with progress percent) and error (red with *ERROR* message).

![Alt text](images/scrape_bar.png?raw=true "Scrape progressbar")
![Alt text](images/error_bar.png?raw=true "Error progressbar")

Bellow progress bar are two buttons: **START** and **STOP**. Button **START** starts process of scraping in the `Scraper`
class, while button **STOP** send *SIGINT* to process started in `Scraper` class.

Logs are also very important aspect of Infobot application. Creating and managing logs is duty of
`Logger` class. 
`Looger` class does not only create logs for scrapping process but for scanning process too.
There are three types of logs:

| type | description |
| :--- | :---------- |
| INFO | events like starting or terminating scraping/scanning process and inserting a new element to database |
| WARNING | events that are not crashing scraping/scanning process but are disturbing it, like not being able to log in on the web page to scrape data |
| ERROR | events that cause scrapping/scanning process to terminate |

> Important: Logs listed on the Home page are **not** only logs from `Scrapper`, but are logs for whole Infobot application

Logs are sorted by the newest, so the fresh logs are always up top.
**INFO** and **WARNING** logs can only be read, while **ERROR** log can be clicked which opens popup
with stack trace of error for more detailed information.

![Alt text](images/trace_log_popup.png?raw=true "Trace log popup")

Data from popup is located in `src/log/application_trace.log` and log data from home page is located in `src/log/application_log.log`.
HTML and JavaScript for home page are located in `home.html` file. Backend logic is located in `home_view.py`.

### Courses

On the courses page there are tree tables: **Watch list**, **Unwatched list** and **Archived list**.

| list | description |
| :--- | :---------- |
Watch | Courses for which corresponding channels exists and which the Scrapper **is** scraping
Unwatched | Courses for which corresponding channels exists and which the Scrapper **is not** scraping
Archived | Courses for which corresponding channels exists but are **archived** and which the Scrapper **is not** scraping

Every list has following elements.

| element | description |
| :--- | :---------- |
Name | Course name 
Tag | Slack channel tag of channel in which Infobot is going to send notifications and reminders
Url | Course url from which Infobot is scrapping data
Watch | Toggle that defines if Infobot is going to scrape data from provided url for course and post messages to the Slack channel
Actions | <ul><li>Save - save changes made for the course</li><li>Reset - reset any changes made on the course (if not saved)</li><li>Archive - archive Slack channel and remove course from the watch list</li><li>Unarchive - unarchive Slack channel (currently not working because Slack bot users can't unarchive channels)</li><li>Delete - delete course from database, but not the channel</li></ul>

HTML and Javascript for this page is located in `course.html` and backend in `course_view.py`.

#### Watch list

![Alt text](images/course_watch_list.png?raw=true "Course Watch list")

List shows all watched courses with option to edit certain attributes of each course.
If users changes *Watch* attribute of the course then that course will move to Unwatched list and if user archives channel that course will go to Archived list.
The last row is made for saving new course to Watch/Unwatched list, so it does not have action buttons for *Archive* and *Delete*.
If there is currently no corresponding channel for a new course user can click on **+** icon in *Tags* section which will
open popup for creating new Slack channel.

![Alt text](images/create_new_channel.png?raw=true "Create a new Slack channel")

When creating channel user can define channel tag, topic and users. Creator of the channel will be Infobot application in the Slack Workspace.

If users whishes not to create special channel for the course then user can select one of the channel tags in the dropdown without creating new channel.
In the channel tag dropdown are shown only channels that have no course connected to it plus channel `#general`.
Channel `#general` can have as many connected courses to it as the user wants.
This behaviour is only present for `#general` channel.

#### Unwatched list

![Alt text](images/course_unwatched_list.png?raw=true "Course Unwatched list")

Unwatched list is almost the same as the Watched list with exception that Unwatched list shows only courses that have *Watch* attribute set to **Off**.
There is still option to edit courses, but not to add any new course like on the Watch list.
If users changes *Watch* attribute of the course then that course will move to Watch list and if user archives channel that course will go to Archived list.
All list elements have all actions available except for courses that have channel tag `#general` which is to prevent user from archiving the `#general` channel.

#### Archived list

![Alt text](images/course_archived_list.png?raw=true "Course Unwatched list")

Archived list contains courses for which channels are archived. For that reason every course has attribute *Watch* set to **Off**.
User can edit every attribute of course except attribute *Watch* which is read only.
In the actions section there is no archive action because channels is already archived but there is option for unarchiving the channel.
Action that unarchives channel is not currently possible because of Slack API and it's limitations for bots.


</details>