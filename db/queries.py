from sqlalchemy.sql import text
from db.models import CodeName, Message, User
from sqlalchemy.orm import session
from db.session import Session


#check and insert new account into the dataBase
def setAccount(userId,userChat):
    session = Session()

    isRegistered = session.query(User).filter(User.UserID==userId).one_or_none()

    if not isRegistered:
        user = User(UserID=userId, userChat=userChat)
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

    user_lang = user.Lang
    return user_lang or 'ar'


def getMessgesIDs(dirs):
    session = Session()

    messages = session.query(Message)\
        .filter(Message.dir==dirs)\
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
        .all()[0]

    return messages

def getDirName(self , dr,lang):
    session = Session()

    code_name = session.query(CodeName)\
        .filter(CodeName.dir.like(f'{dr}%'))\
        .one_or_none()

    lang = getattr(code_name, lang)

    return lang

