#!/usr/bin/env python
from __future__ import annotations

from enum import Enum
from typing import NoReturn, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import engine
from zaimcsvconverter.enum import FileCsvConvert, Account
from zaimcsvconverter.session_manager import SessionManager

Base: DeclarativeMeta = declarative_base()


class Index(Enum):
    NAME: int = 0
    NAME_ZAIM: int = 1
    CATEGORY_PAYMENT_LARGE: int = 2
    CATEGORY_PAYMENT_SMALL: int = 3
    CATEGORY_INCOME: int = 4
    TRANSFER_ACCOUNT: int = 5


class Store(Base):
    __tablename__: str = 'stores'

    id: Column = Column(Integer, primary_key=True)
    account_id: Column = Column(Integer)
    name: Column = Column(String(255), unique=True)
    name_zaim: Column = Column(String(255))
    category_payment_large: Column = Column(String(255))
    category_payment_small: Column = Column(String(255))
    category_income: Column = Column(String(255))
    transfer_target: Column = Column(String(255))
    STORE_KIND_WAON: int = 1
    STORE_KIND_GOLD_POINT_CARD_PLUS: int = 2

    def __init__(self, account: Account, list_row_store: list):
        self.account_id: int = account.value
        self.name: str = list_row_store[Index.NAME.value]
        self.name_zaim: str = self.get_str_or_none(list_row_store, Index.NAME_ZAIM.value)
        self.category_payment_large: str = self.get_str_or_none(list_row_store,
                                                                Index.CATEGORY_PAYMENT_LARGE.value)
        self.category_payment_small: str = self.get_str_or_none(list_row_store,
                                                                Index.CATEGORY_PAYMENT_SMALL.value)
        self.category_income: str = self.get_str_or_none(list_row_store, Index.CATEGORY_INCOME.value)
        self.transfer_target: str = self.get_str_or_none(list_row_store, Index.TRANSFER_ACCOUNT.value)

    @staticmethod
    def get_str_or_none(li: list, index: int) -> str:
        return li[index] if index < len(li) and li[index] is not '' else None

    @staticmethod
    def try_to_find(account: Account, store_name: str) -> Store:
        try:
            return Store.find(account, store_name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        try:
            return Store.find(account, store_name.replace("−", "ー"))
        except NoResultFound as e:
            file_csv_convert = FileCsvConvert.create(account)
            raise KeyError(
                f'"{store_name}" is not defined on {file_csv_convert.value}. ' + 'Please define it.'
            ) from e

    @staticmethod
    def find(account: Account, store_name: str) -> Store:
        with SessionManager() as session:
            return session.query(Store).filter(
                Store.account_id == account.value,
                Store.name == store_name
            ).one()

    @staticmethod
    def save_all(stores: List[Store]) -> NoReturn:
        with SessionManager() as session:
            with session.begin():
                session.add_all(stores)


def initialize_database(target_engine=engine) -> NoReturn:
    Base.metadata.create_all(target_engine, checkfirst=False)
