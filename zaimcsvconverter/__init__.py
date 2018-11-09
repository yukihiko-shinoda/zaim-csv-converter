import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zaimcsvconverter.config import Config

engine = create_engine('sqlite://')
Session = sessionmaker(bind=engine, autocommit=True)
FILE_CONFIG = './config.yml'
CONFIG = Config(FILE_CONFIG)
