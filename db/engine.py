import os
from sqlalchemy import create_engine


engine = create_engine(f'sqlite:///fmsi-bot.db', echo=True)