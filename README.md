# lessons_report
 
Script allows to receive status messages from Telegram bot about checked Devman lessons.

## Installation

Project tested under Python version **3.11.9**.  
Python3 should already be installed.  
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Telegram bot will be needed for sending messages. Create bot via [@BotFather](https://t.me/BotFather).  
Bot token looks like: 1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx.

Security sensitive information highly recommended to store in environmental variables.  
Example of `.env` file:
```
# Your personal token from Devman API
DVMN_API_TOKEN = 0000000x0xxxx0x0x000x000xx0000x00xxx0xx0

# Token of your Telegram bot
TG_BOT_TOKEN = 1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx

# Telegram chat ID of the message receiver
TG_CHAT_ID = 000000000

# Time in seconds which request will wait for server response.
# Have to be greater then server response timeout.
# Present server response timeout is 90 seconds, but can change.
REQUEST_TIMEOUT = 120
```

## Usage

Just run script and it will poll server infinitely and send Telegram messages on server response.
```
$ py lessons_report.py
```

## Project Goals
The code is written for educational purposes on online-course for web-developers dvmn.org.
