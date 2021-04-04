"""This module implements SQLAlchemy database models."""
from __future__ import annotations

import warnings
from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, Type, TypeVar

from inflector import Inflector
from sqlalchemy import Column, Integer, String, UniqueConstraint, exc
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from sqlalchemy.orm.exc import NoResultFound

from zaimcsvconverter import Session
from zaimcsvconverter.session_manager import SessionManager


class FileCsvConvertId(Enum):
    """This class implements file for CSV convert id on database."""

    WAON = 1
    GOLD_POINT_CARD_PLUS = 2
    MUFG = 3
    SF_CARD_VIEWER = 4
    AMAZON = 5
    VIEW_CARD = 6
    PAY_PAL = 7

    @property
    def value(self) -> int:
        """This method overwrite super method for type hint."""
        return super().value


Base: DeclarativeMeta = declarative_base()

# noinspection Pylint
TypeVarBase = TypeVar("TypeVarBase", bound=Base)


@dataclass
class ConvertTableRowData:
    """This class implements abstract data class for wrapping list of convert table row model."""

    name: str


@dataclass
class StoreRowData(ConvertTableRowData):
    """This class implements data class for wrapping list of store convert table row model."""

    name_zaim: Optional[str] = None
    category_payment_large: Optional[str] = None
    category_payment_small: Optional[str] = None
    category_income: Optional[str] = None
    transfer_account: Optional[str] = None


@dataclass
class ItemRowData(ConvertTableRowData):
    """This class implements data class for wrapping list of item and category row model."""

    category_payment_large: Optional[str] = None
    category_payment_small: Optional[str] = None


TypeVarConvertTableRowData = TypeVar("TypeVarConvertTableRowData", bound=ConvertTableRowData)


class ConvertTableRecordMixin:
    """
    This class implements convert table mixin.
    @see https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
    """

    @declared_attr
    def __tablename__(self):
        return Inflector().pluralize(self.__name__.lower())

    id: Column = Column(Integer, primary_key=True)
    file_csv_convert_id: Column = Column(Integer)
    name: Column = Column(String(255))
    category_payment_large: Column = Column(String(255))
    category_payment_small: Column = Column(String(255))

    __table_args__ = (UniqueConstraint("file_csv_convert_id", "name", name="_name_on_each_account_uc"),)

    @abstractmethod
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: TypeVarConvertTableRowData):
        self.file_csv_convert_id: int = file_csv_convert_id.value
        self.name: str = row_data.name

    @staticmethod
    def _get_str_or_none(value: Optional[str]) -> Optional[str]:
        return value if value != "" else None

    @classmethod
    def try_to_find(
        cls: Type[ConvertTableRecordMixin], file_csv_convert_id: FileCsvConvertId, name: str
    ) -> TypeVarBase:
        """This method select Store model from database. If record is not exist, raise NoResultFound."""
        try:
            return cls.find(file_csv_convert_id, name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        return cls.find(file_csv_convert_id, name.replace("−", "ー"))

    @classmethod
    def find(cls: Type[ConvertTableRecordMixin], file_csv_convert_id: FileCsvConvertId, name: str) -> TypeVarBase:
        """This method select Store model from database."""
        with SessionManager() as session:
            return (
                session.query(cls).filter(cls.file_csv_convert_id == file_csv_convert_id.value, cls.name == name).one()
            )

    @classmethod
    def save_all(cls: Type[TypeVarBase], models: List[TypeVarBase]) -> None:
        """This method insert Store models into database."""
        with SessionManager() as session:
            with session.begin():
                session.add_all(models)


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=exc.SAWarning)

    class Store(Base, ConvertTableRecordMixin):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        name_zaim: Column = Column(String(255))
        category_income: Column = Column(String(255))
        transfer_target: Column = Column(String(255))

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: StoreRowData):
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            self.name_zaim: Optional[str] = self._get_str_or_none(row_data.name_zaim)
            self.category_payment_large: Optional[str] = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_small: Optional[str] = self._get_str_or_none(row_data.category_payment_small)
            self.category_income: Optional[str] = self._get_str_or_none(row_data.category_income)
            self.transfer_target: Optional[str] = self._get_str_or_none(row_data.transfer_account)

        @property
        def is_amazon(self) -> bool:
            """This property returns whether this store is Amazon.co.jp or not."""
            return self.name in {"Ａｍａｚｏｎ  Ｄｏｗｎｌｏａｄｓ", "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ", "ＡＭＡＺＯＮ．ＣＯ．ＪＰ"}

    class Item(Base, ConvertTableRecordMixin):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: ItemRowData):
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            self.category_payment_large: Optional[str] = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_small: Optional[str] = self._get_str_or_none(row_data.category_payment_small)


def initialize_database() -> None:
    """This function create empty tables from SQLAlchemy models."""
    # pylint: disable=no-member
    Base.metadata.create_all(Session.get_bind(), checkfirst=False)


@dataclass
class ClassConvertTable(Generic[TypeVarConvertTableRowData]):
    """This class implements association of classes about convert table."""

    model: Type[ConvertTableRecordMixin]
    row_data: Type[TypeVarConvertTableRowData]


class ConvertTableType(Enum):
    """This class implements types of convert table."""

    STORE = ClassConvertTable(Store, StoreRowData)
    ITEM = ClassConvertTable(Item, ItemRowData)

    @property
    def value(self) -> ClassConvertTable:
        """This method overwrite super method for type hint."""
        return super().value
