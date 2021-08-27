from sqlalchemy.orm import  sessionmaker
from db.engine import engine

Session = sessionmaker(bind=engine, autoflush=False)
