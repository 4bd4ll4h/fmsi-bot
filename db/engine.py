import json
import os
from sqlalchemy import create_engine

scriptPath = os.path.abspath(__file__)
dirPath = os.path.dirname(scriptPath)
configPath = os.path.join(dirPath.replace('db',''),'config.json')

config = json.load(open(configPath,encoding='utf8'))
engine = create_engine(f'sqlite:///{config["database"]}', echo=True)