#!/usr/bin/env python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from zaimcsvconverter import engine

Base = declarative_base()


class WaonStore(Base):
    __tablename__ = 'waon_stores'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    name_zaim = Column(String(255))
    category_large = Column(String(255))
    category_small = Column(String(255))

    INDEX_STORE_WAON = 0
    INDEX_STORE_ZAIM = 1
    INDEX_CATEGORY_LARGE = 2
    INDEX_CATEGORY_SMALL = 3

    def __init__(self, name, name_zaim, category_large=None, category_small=None):
        self.name = name
        self.name_zaim = name_zaim
        self.category_large = category_large
        self.category_small = category_small

    def convert_to_tuple(self):
        return self.name, self.name_zaim, self.category_large, self.category_small


def initialize_database(target_engine=engine):
    Base.metadata.create_all(target_engine, checkfirst=False)
