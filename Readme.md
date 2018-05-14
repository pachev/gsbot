# Gear Score Bot for Black Desert Online
[![Travis Build](https://travis-ci.org/pachev/gsbot.svg?branch=master)]()
[![Discord Server](https://img.shields.io/discord/417173590757212162.svg)](https://discord.gg/STa7Ebz)

#### [A Discord Bot][2]


### Description

A python application to help manage guild members and their gear score for 
Black Desert Online. This specific bot is made for Sazerac guild but can be
adjusted for use with any other guild. The link to view this data visually
is at [https://gsbot.pachevjoseph.com](https://gsbot.pachevjoseph.com)


### Requirements
- Python 3.6+
- Mongodb
- discord.py

## Installation


### Python Virtual Environment

This project is best ran in a virtual environment. You can use [pyvenv][3],
which comes with python 3 and greater. The virtual enviroment lets you run
different versions of python and packages from other projects.

#### Installation (Unix)

First install python3+ on your machine which should come with [pip][4]. If
not, download from link provided.

1. `python3 -m venv env` - Create a virtual environment in the env folder
2. `source env/bin/activate` - Load the environment
3. `pip install -r requirements.txt` - Install dependencies
4. `deactivate` - Unloads the environment


#### Installation (Windows)
Note - Most documentation is for unix systems. Differences between windows and unix are: `env\Scripts\` instead of `env/bin/` and libraries go in `env\Lib\` rather than `env/lib/`)

First install python3+ on your machine and then download and install [pip][4].
Then from the root of the project run:

1. `pip install virtualenv` - Install virtualenv if not already done soCreate a virtual environment in the venv folder
2. `virtualenv venv` - This creates will create a series of directories and scripts
3. `venv/Scripts/activate` - Load the enviroment (There should be a (venv) before the current directory path name
4. `pip install -r requirements.txt` - Install dependencies
5. `deactivate` - Unloads the environment

## Running

Once your dependencies are installed, there are a couple of steps you need to do before running.

1. create a`config.ini` file inside of the main directory
2. Setup config file like the example below: If you would like to give your
users the ability to attach files directly when updating gear pictures, then
create a [cloudinary][5] account and fill out the fields appropriately under 'cloudinary'
settings

```ini
[auth]
token = ... #This is where you put your bot token that you get from discord
user = user
pwd = pwd

[cloudinary]
has_cloud_storage = False
cloud_name = some_name
api_key = some_api_key
api_secret = some_api_secret

[db]
name = gsbot
port = 27017
host = localhost
character_collection = character
server_collection = server
member_collection = member
historical_collection = historical
```

3. Have an instance of mongodb running with the a db that has the same name
that is inside of the config file. The bot, as it stands, is configured to connect to
a localhost instance of mongo on port 27017. If you would like different configurations,
make sure you change the config file accordingly.



### Thanks to
A python application using [discord.py][1]

[1]: https://github.com/Rapptz/discord.py
[2]: https://bots.discord.pw/
[3]: https://docs.python.org/3/library/venv.html
[4]: https://pip.pypa.io/en/latest/installing/
[5]: https://cloudinary.com/
