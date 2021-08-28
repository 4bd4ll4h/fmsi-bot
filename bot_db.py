import os,json,sqlite3

from telebot.types import Message

config = json.load(open('config.json'))
database= config['database']

if os.path.exists(database):
    print(' Database already exists.')
else:
    conn=sqlite3.connect(database)
    print("[+] Database opened successfully.")

    conn.execute(''' CREATE TABLE users
            (UserID INTEGER PRIMARY KEY,
            Lev INTEGER,
            SIndex TEXT,
            name TEXT,
            News TEXT DEFAULT "false",
            Lang TEXT DEFAULT "ar",
            PatchNews TEXT DEFAULT "true",
            userChat TEXT);''')
    conn.commit()
    print('[+] Table users created successfully.')

    conn.execute(''' CREATE TABLE messages
                (dir TEXT,
                messageId TEXT,
                chatId TEXT,
                content_type TEXT)''')
    print('[+] Table messeges Created.')

    conn.execute(''' CREATE TABLE codeNames(
        dir TEXT PRIMARY KEY,
        ar TEXT,
        en TEXT 
    )''')
    print('[+] Table codeNames Created.')
conn.close
