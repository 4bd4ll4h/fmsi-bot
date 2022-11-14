![image](https://github.com/4bd4ll4h/fmsi-bot/blob/main/header.svg)  
#### Note This bot is no longer working due to maintainability issues and developer busyness, but you can refer to this [bot](https://t.me/IT016Bot) which do almost the same job. Made by [A.M. Elkheir ](https://github.com/am-elkheir)

# FMSI bot

FMSI bot is a telegram bot for students of [faculty of mathematical science and informatics](https://fms.uofk.edu/en) aka **School of math** to help them communicate and study more effectively. This bot designed to reduce the time of collecting and organizing course martials and bridging the gap between teachers and students.

It also provides a way of communication between batches which will help in delivering news and decision-making

## Features

- A directory system that organizes course martials based on their types and in which semester they're taught.  
  Ex: _sem7/cs403/references_
- The bot gives admins the ability to send messages to all (or some) students to keep them updated with various news (university event, lectures time change, assignment, etc.)

- Multi language support (currently Arabic and English, but scaling is easy)
- A hot key for accessing current semester courses and their new materials
- A help section on how to use the bot

## Installation

First, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements from the text file.

```bash
pip install -r requirement.txt
```

Second, fill the config file with your own information.

Finally, make a private telegram group chat and add your bot as an admin. After that you can use the admin commands to make directories and upload files and send broadcast messages

## How it works

FMSI bot is built with [pyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI) as telegram API library and SQLite to store the files and users info.

A telegram group chat containing the bot and admin members. Bot admins send files in this group and specify the file directory. Then, the bot stores this info in its database and preforms a mapping between the files and their directories for regular users. Other commands are available for admins to _update, delete files and directory and to send broadcast messages and polls_
