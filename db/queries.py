import re
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import user
from telebot import types
from db.models import CodeName, Message, User
from sqlalchemy.orm import session
from db.session import Session


def isNewUser(id):
    session = Session()
    isRegistered = session.query(User).filter(User.UserID==id).one_or_none()
    return not bool(isRegistered)

#check and insert new account into the dataBase
def setAccount(userId,userChat,lang):
    session = Session()
    isRegistered = session.query(User).filter(User.UserID==userId).one_or_none()
    if not isRegistered:
        user = User(UserID=userId, userChat=userChat,Lang=lang)
        session.add(user)
        session.commit()
    
    return bool(isRegistered)


#set the Student grade Level
def setLev(lev, userId):
    session = Session()

    user = session.query(User).filter(User.UserID==userId).one()
    user.Lev = lev

    session.commit()
    session.close()

def getSubUser(patch:str):
    session = Session()

    users = session.query(User)\
        .filter(User.PatchNews=='true', User.Lev==str(patch))\
        .all()

    return users

def setUserInfo(userId, column, data):
    session = Session()

    user = session.query(User)\
        .filter(User.UserID==userId).one_or_none()
    
    setattr(user, column, data)

    session.commit()
    session.close()

def setIndex(userId, index):
    session = Session()

    user = session.query(User)\
        .filter(User.UserID==userId).one_or_none()
    
    user.SIndex = index

    session.commit()
    session.close()


def checkInfo(userId,info):
    session = Session()

    user = session.query(User)\
        .filter(User.UserID==userId).one_or_none()

    column_data = getattr(user, info)

    
    return bool(column_data)


def getLanguage(userId):
    session = Session()

    user = session.query(User)\
        .filter(User.UserID==userId).one_or_none()
    if user:
        user_lang = user.Lang
        return user_lang or 'ar'
    return 'ar'


def getMessgesIDs(dirs):
    session = Session()

    messages = session.query(Message)\
        .filter(Message.dir==dirs,Message.messageId!='null')\
        .all()

    return messages


def checkDirCode(d):
    session = Session()

    code_name = session.query(CodeName)\
        .filter(CodeName.dir==d)\
        .one_or_none()

    if code_name:
        if not code_name.ar:
            return ['ar']
        elif not code_name.en:
            return ['en']
    else:
        return ['ar','en']
    return True

def insertMessageId(dirs,chatId,messageId,content_type):
    session = Session()

    message = Message(dir=dirs, messageId=messageId, chatId=chatId, content_type=content_type)

    session.add(message)
    session.commit()

    session.close()


def setDir( lang, dirs, name):
    session = Session()

    sql = text(f'''
INSERT INTO codeNames (dir, {lang})
        VALUES
            ("{dirs}","{name}")
            ON CONFLICT(dir)
            DO UPDATE SET {lang}="{name}";
    ''')

    try:
        session.execute(sql)
        session.commit()
        return True
    except:
        return False


def getMessagesDir(dirs):
    session = Session()

    messages = session.query(Message)\
        .filter(Message.dir.like(f'{dirs}%'))\
        .all()
    if messages:
        return messages
    else :return None

def getDirName(dr,lang):
    session = Session()
    code_name = session.query(CodeName)\
        .filter(CodeName.dir.like(f'{dr}'))\
        .one_or_none()

    lang = getattr(code_name, lang)

    return lang

def UpdateDir(dirc,newName,column):
    """it's an update method for codeNames table for spcific column with new name
    -retrun true in scusse , false in failure"""
    session = Session()

    try:
        code_name = session.query(CodeName)\
            .filter(CodeName.dir.like(f'{dirc}'))\
            .one_or_none()

        setattr(code_name, column, newName)

        session.commit()

        return True

    except:
        return False

def deleteDiractory(dirc):
    """simply delete this dir from codeNames table"""
    session = Session()

    code_name = session.query(CodeName)\
            .filter(CodeName.dir==dirc)\
            .one_or_none()

    session.delete(code_name)

    session.commit()

def deleteDBMessage(chatID,fileId:str):
    """function to delete row in the messges table that contin the same messageID"""
    session = Session()

    message = session.query(Message)\
        .filter(Message.messageId==fileId)\
        .one_or_none()

    session.delete(message)
    session.commit()
def isFileExsit(fileId:str):
    """function to delete row in the messges table that contin the same messageID"""
    session = Session()

    message = session.query(Message)\
        .filter(Message.messageId==fileId)\
        .one_or_none()
    return True if message else False


def getNewsSubUsers():
    """get all user where News Column is true"""
    session = Session()

    users = session.query(User)\
        .filter(User.News=='true')\
        .all()

    return users