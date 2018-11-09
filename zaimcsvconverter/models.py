#!/usr/bin/env python

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from zaimcsvconverter import engine

Base = declarative_base()


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    store_kind_id = Column(Integer)
    name = Column(String(255), unique=True)
    name_zaim = Column(String(255))
    category_large = Column(String(255))
    category_small = Column(String(255))
    STORE_KIND_WAON = 1
    STORE_KIND_GOLD_POINT_CARD_PLUS = 2

    def __init__(self, store_kind_id, name, name_zaim, category_large=None, category_small=None):
        self.store_kind_id = store_kind_id
        self.name = name
        self.name_zaim = name_zaim
        self.category_large = category_large
        self.category_small = category_small


def initialize_database(target_engine=engine):
    Base.metadata.create_all(target_engine, checkfirst=False)
