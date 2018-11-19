#!/usr/bin/env python

"""
This module implements SQLAlchemy database models.
"""

from __future__ import annotations

from typing import NoReturn, List, TYPE_CHECKING, Type, TypeVar

from inflector import Inflector
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta, declared_attr
from sqlalchemy.orm.exc import NoResultFound

from dataclasses import dataclass

from zaimcsvconverter import ENGINE
from zaimcsvconverter.session_manager import SessionManager
if TYPE_CHECKING:
    from zaimcsvconverter.account_dependency import Account, AccountDependency

Base: DeclarativeMeta = declarative_base()

# noinspection Pylint
T: TypeVar = TypeVar('T')


class ConvertTableMixin:
    """This class implements convert table mixin."""
    @declared_attr
    def __tablename__(self):
        return Inflector().pluralize(self.__name__.lower())

    id: Column = Column(Integer, primary_key=True)
    account_id: Column = Column(Integer)
    name: Column = Column(String(255))
    category_payment_large: Column = Column(String(255))
    category_payment_small: Column = Column(String(255))

    __table_args__ = (UniqueConstraint('account_id', 'name', name='_name_on_each_account_uc'),)

    @staticmethod
    def _get_str_or_none(value: str) -> str:
        return value if value != '' else None

    @classmethod
    def try_to_find(cls: Type[T], account_dependency: AccountDependency, name: str) -> T:
        """
        This method select Store model from database. If record is not exist, raise NoResultFound.
        """
        try:
            return cls.find(account_dependency, name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        try:
            return cls.find(account_dependency, name.replace("−", "ー"))
        except NoResultFound:
            return None

    @classmethod
    def find(cls: Type[T], account_dependency: 'AccountDependency', name: str) -> T:
        """
        This method select Store model from database.
        """
        with SessionManager() as session:
            return session.query(cls).filter(
                cls.account_id == account_dependency.id,
                cls.name == name
            ).one()

    @classmethod
    def save_all(cls: Type[T], models: List[T]) -> NoReturn:
        """
        This method insert Store models into database.
        """
        with SessionManager() as session:
            with session.begin():
                session.add_all(models)


@dataclass
class StoreRowData:
    """This class implements data class for wrapping list of store convert table row model."""
    name: str
    name_zaim: str = None
    category_payment_large: str = None
    category_payment_small: str = None
    category_income: str = None
    transfer_account: str = None


class Store(Base, ConvertTableMixin):
    """
    This class implements Store model to convert from account CSV to Zaim CSV.
    """
    name_zaim: Column = Column(String(255))
    category_income: Column = Column(String(255))
    transfer_target: Column = Column(String(255))

    def __init__(self, account: 'Account', row_data: StoreRowData):
        self.account_id: int = account.value.id
        self.name: str = row_data.name
        self.name_zaim: str = self._get_str_or_none(row_data.name_zaim)
        self.category_payment_large: str = self._get_str_or_none(row_data.category_payment_large)
        self.category_payment_small: str = self._get_str_or_none(row_data.category_payment_small)
        self.category_income: str = self._get_str_or_none(row_data.category_income)
        self.transfer_target: str = self._get_str_or_none(row_data.transfer_account)


@dataclass
class ItemRowData:
    """This class implements data class for wrapping list of item and category row model."""
    name: str
    category_payment_large: str = None
    category_payment_small: str = None


class Item(Base, ConvertTableMixin):
    """
    This class implements Store model to convert from account CSV to Zaim CSV.
    """

    def __init__(self, account: 'Account', row_data: ItemRowData):
        self.account_id: int = account.value.id
        self.name: str = row_data.name
        self.category_payment_large: str = self._get_str_or_none(row_data.category_payment_large)
        self.category_payment_small: str = self._get_str_or_none(row_data.category_payment_small)


def initialize_database(target_engine=ENGINE) -> NoReturn:
    """
    This function create empty tables from SQLAlchemy models.
    """
    Base.metadata.create_all(target_engine, checkfirst=False)
