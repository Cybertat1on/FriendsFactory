[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/fabrika/app?startapp=ref_2008453)
[![Static Badge](https://img.shields.io/badge/Telegram-Channel-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/CyberToolz)

#  Bot for FriendsFactroy

![start-fabrika](https://github.com/user-attachments/assets/1e3ac93a-d7d7-410a-aaf2-70fb661eb336)


# 🔥🔥 PYTHON version must be 3.10 - 3.11.5 🔥🔥

> 🇷 🇺 README in russian available [here](README-RU.md)
## Features  
| Feature                                                   				|     Supported    |
|---------------------------------------------------------------------------|:----------------:|
| Multithreading                                            			    |        ✔️        |
| Proxy binding to session                                  			    |        ✔️        |
| Auto Referral                                                  		    |        ✔️        |
| Auto Tap                                                   				|        ✔️        |
| Auto Boost                                                 			    |        ✔️        |
| Auto manage factory (buy worker, send worker to work, claim worker reward)|        ✔️        |
| Auto Tasks                                                   				|        ✔️        |
| Support for pyrogram .session                     						|        ✔️        |

## [Settings](https://github.com/Cybertat1on/FriendsFactory.git/blob/main/.env-example)
| Settings 				   	     	                      |												 Description 											 |
|----------------------------------------------|:-------------------------------------------------------------------------------------------------------:|
| **API_ID / API_HASH**                        | Platform data from which to run the Telegram session (default - android)                                      |       
| **REF_LINK**                                 | Put your ref link here (10% for me)			                                                             |
| **AUTO_TASK**                                | Auto do tasks (default: True)                                                                                 |
| **AUTO_TAP**                                 | Auto tap to earn point (default: True)                                                                        |
| **AUTO_BOOST**                               | Auto use full energy boost (default: True)                                                                    |
| **TAP_COUNT**                                | Random ammount of taps (default: [30, 75])                                                                    |
| **SLEEP_BY_MIN_ENERGY**                      | Minium energy to sleep (default: 100)                                                                         |
| **SLEEP_BETWEEN_TAPS**                       | Random sleep time between each taps (default: [15, 30])                                                       |
| **AUTO_MANAGE_FACTORY**                      | Auto manage factory (default: True)                                                                           |
| **AUTO_BUY_WORKER**                          | Auto Buy worker (default: True)                                                                               |
| **MAX_NUMBER_OF_WORKER_TO_BUY**              | Max number of worker (without protection) to buy (default: 3)                                           |
| **AUTO_BUY_WORKING_PLACE**                   | Auto buy workplaces (default: True)                                                       |
| **MAX_NUMBER_OF_WORKING_PLACE_TO_BUY**       | Max workplaces to buy (default: 10 - Max is 20)                                                       |
| **USE_PROXY_FROM_FILE**                      | Whether to use a proxy from the bot/config/proxies.txt file (True / False)                                    |




## Quick Start 📚

To fast install libraries and run bot - open `run.bat` on **Windows** or `run.sh` on **Linux**

## Prerequisites
Before you begin, make sure you have the following installed:
- [**Python**](https://www.python.org/downloads/release/python-3100/) **version 3.10**

## Obtaining API Keys
1. Go to [**my.telegram.org**](https://my.telegram.org/auth) and log in using your phone number.
2. Select `API development tools` and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` provided after registering your application in the `.env` file.

## Installation
You can download the [**repository**](https://github.com/Cybertat1on/FriendsFactory) by cloning it to your system and installing the necessary dependencies:
```shell
git clone https://github.com/Cybertat1on/FriendsFactory.git
cd FriendsFactory
```

Then you can do automatic installation by typing:

Windows:
```shell
run.bat
```

Linux:
```shell
run.sh
```

# Linux manual installation
```shell
sudo sh install.sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
```

You can also use arguments for quick start, for example:
```shell
~/FriendsFactory >>> python3 main.py --action (1/2)
# Or
~/FriendsFactory >>> python3 main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
```

You can also use arguments for quick start, for example:
```shell
~/FriendsFactory >>> python main.py --action (1/2)
# Or
~/FriendsFactory >>> python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session
```

# Termux manual installation
```
> pkg update && pkg upgrade -y
> pkg install python rust git -y
> git clone https://github.com/Cybertat1on/FriendsFactory.git
> cd Fabrika-Friends-Factory
> pip install -r requirements.txt
> python main.py
```

You can also use arguments for quick start, for example:
```termux
~/FriendsFactory > python main.py --action (1/2)
# Or
~/FriendsFactory > python main.py -a (1/2)

# 1 - Run clicker
# 2 - Creates a session 
```

