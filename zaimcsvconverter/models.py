#!/usr/bin/env python

"""
This module implements SQLAlchemy database models.
"""

from __future__ import annotations

from typing import NoReturn, List, TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound

from dataclasses import dataclass

from zaimcsvconverter import ENGINE
from zaimcsvconverter.session_manager import SessionManager
if TYPE_CHECKING:
    from zaimcsvconverter.enum import Account, AccountDependency

Base: DeclarativeMeta = declarative_base()


@dataclass
class StoreRowData:
    """This class implements data class for wrapping list of GOLD POINT CARD+ CSV row model."""
    name: str
    name_zaim: str = None
    category_payment_large: str = None
    category_payment_small: str = None
    category_income: str = None
    transfer_account: str = None


class Store(Base):
    """
    This class implements Store model to convert from account CSV to Zaim CSV.
    """
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

    def __init__(self, account: 'Account', row_data: StoreRowData):
        self.account_id: int = account.value.id
        self.name: str = row_data.name
        self.name_zaim: str = self._get_str_or_none(row_data.name_zaim)
        self.category_payment_large: str = self._get_str_or_none(row_data.category_payment_large)
        self.category_payment_small: str = self._get_str_or_none(row_data.category_payment_small)
        self.category_income: str = self._get_str_or_none(row_data.category_income)
        self.transfer_target: str = self._get_str_or_none(row_data.transfer_account)

    @staticmethod
    def _get_str_or_none(value: str) -> str:
        return value if value != '' else None

    @staticmethod
    def try_to_find(account_dependency: AccountDependency, store_name: str) -> Store:
        """
        This method select Store model from database. If record is not exist, raise NoResultFound.
        """
        try:
            return Store.find(account_dependency, store_name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        try:
            return Store.find(account_dependency, store_name.replace("−", "ー"))
        except NoResultFound as error:
            raise KeyError(
                f'"{store_name}" is not defined on {account_dependency.file_name_csv_convert}. ' + 'Please define it.'
            ) from error

    @staticmethod
    def find(account_dependency: 'AccountDependency', store_name: str) -> Store:
        """
        This method select Store model from database.
        """
        with SessionManager() as session:
            return session.query(Store).filter(
                Store.account_id == account_dependency.id,
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
