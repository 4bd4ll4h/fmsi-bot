![image](https://github.com/am-elkheir/fmsi-bot/blob/main/header.svg)  

#### Note This bot is no longer working due to maintainability issues and developer busyness, but you can refer to this [bot](https://t.me/IT016Bot) which do almost the same job. Made by [A.M. Elkheir ](https://github.com/am-elkheir)


# FMSI bot 
FMSI bot is a telegram bot for students of [faculty of mathematical science and informatics](https://fms.uofk.edu/en) aka **School of math** to help them communicate and study more effectively. This bot designed with the intentions of reducing the time of collecting and organizing courses martial and bridging the gap between the teacher and the students.

It also provides a way of communication between batches which will help in delivering news and decision-making

## Features
- A directory system that organize college courses martial based on their types and in which semester they belong.  
 Ex: _sem7/cs403/references_
- The bot give the admins ability to send news messages for all students or a specific group of students to keep them updated with the various update like (university event, lectures time change, assignment, etc.)  

- Multi language support (currently Arabic and English, but scaling is easy)
- A hot key for accessing your current semester courses and their new materials 
- A help section that helps you how to use the bot

## Installation

First, use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirement library from the requirement text file.

```bash
pip install -r requirement.txt
```
Second, fill the config file with your own info and telegram bot token  

Finally, make a private telegram group and add your bot as an admin after that you can use the admin commands to make directories and upload file and send broadcast messages  

## How it works
FMSI bot build with the help of [pyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI) as telegram API library and SQLite to store the telegram file info and users info.  

A telegram group that only the bot admins are members of and the bot is admin of the group. Bot admins send files in this group and specify the file directory, then the bot store this info in its database and preform a mapping between files and their directory for regular users. Other commands are available for admins to *update, delete files and directory and to send broadcast messages and bolls*

