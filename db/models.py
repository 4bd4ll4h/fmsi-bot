from sqlalchemy import Column, Integer, String, Sequence
from db.engine import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    UserID = Column(Integer,Sequence('user_id_seq'), primary_key=True )
    Lev = Column(String(50))
    SIndex = Column(String(10))
    name = Column(String(100))
    News = Column(String(10), default="false")
    Lang = Column(String(5), default="ar")
    PatchNews = Column(String(10), default="true")
    userChat = Column(String(200))

    def __repr__(self):
        return f"<User(name='{self.name}')>"

class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer,Sequence('user_id_seq'), primary_key=True )

    dir = Column(String(200))
    messageId = Column(String(200))
    chatId = Column(String(200))
    content_type = Column(String(50))

    def __repr__(self):
        return f"<Message(messageId='{self.messageId}', content_type='{self.content_type}')>"

class CodeName(Base):
    __tablename__ = 'codeNames'

    dir = Column(String(200), primary_key=True )
    ar = Column(String(200))
    en = Column(String(200))

    def __repr__(self):
        return f"<CodeName(dir='{self.dir}')>"

Base.metadata.create_all(engine)