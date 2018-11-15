#!/usr/bin/env python

"""
This module implements SQLAlchemy database models.
"""

from __future__ import annotations

from enum import Enum
from typing import NoReturn, List
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import ENGINE
from zaimcsvconverter.enum import FileCsvConvert, Account
from zaimcsvconverter.session_manager import SessionManager

Base: DeclarativeMeta = declarative_base()


class Store(Base):
    """
    This class implements Store model to convert from account CSV to Zaim CSV.
    """
    class Index(Enum):
        """
        This class implements constants of index for row of convert table CSV.
        """
        NAME: int = 0
        NAME_ZAIM: int = 1
        CATEGORY_PAYMENT_LARGE: int = 2
        CATEGORY_PAYMENT_SMALL: int = 3
        CATEGORY_INCOME: int = 4
        TRANSFER_ACCOUNT: int = 5

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
        self.name: str = list_row_store[Store.Index.NAME.value]
        self.name_zaim: str = self._get_str_or_none(list_row_store, Store.Index.NAME_ZAIM.value)
        self.category_payment_large: str = self._get_str_or_none(list_row_store,
                                                                 Store.Index.CATEGORY_PAYMENT_LARGE.value)
        self.category_payment_small: str = self._get_str_or_none(list_row_store,
                                                                 Store.Index.CATEGORY_PAYMENT_SMALL.value)
        self.category_income: str = self._get_str_or_none(list_row_store, Store.Index.CATEGORY_INCOME.value)
        self.transfer_target: str = self._get_str_or_none(list_row_store, Store.Index.TRANSFER_ACCOUNT.value)

    @staticmethod
    def _get_str_or_none(argument_list: list, index: int) -> str:
        return argument_list[index] if index < len(argument_list) and argument_list[index] != '' else None

    @staticmethod
    def try_to_find(account: Account, store_name: str) -> Store:
        """
        This method select Store model from database. If record is not exist, raise NoResultFound.
        """
        try:
            return Store.find(account, store_name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        try:
            return Store.find(account, store_name.replace("−", "ー"))
        except NoResultFound as error:
            file_csv_convert = FileCsvConvert.create(account)
            raise KeyError(
                f'"{store_name}" is not defined on {file_csv_convert.value}. ' + 'Please define it.'
            ) from error

    @staticmethod
    def find(account: Account, store_name: str) -> Store:
        """
        This method select Store model from database.
        """
        with SessionManager() as session:
            return session.query(Store).filter(
                Store.account_id == account.value,
                Store.name == store_name
            ).one()

    @staticmethod
    def save_all(stores: List[Store]) -> NoReturn:
        """
        This method insert Store models into database.
        """
        with SessionManager() as session:
            with session.begin():
                session.add_all(stores)


def initialize_database(target_engine=ENGINE) -> NoReturn:
    """
    This function create empty tables from SQLAlchemy models.
    """
    Base.metadata.create_all(target_engine, checkfirst=False)
