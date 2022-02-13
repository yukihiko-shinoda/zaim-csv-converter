"""This module implements SQLAlchemy database models."""
from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
import re
from types import DynamicClassAttribute
from typing import Any, cast, Generic, List, Optional, Type, TypeVar
import warnings

from inflector import Inflector
from sqlalchemy import Column, exc, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr

# Reason: Since stub for SQLAlchemy lacks.
from sqlalchemy.orm.decl_api import DeclarativeMeta, registry  # type: ignore
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

    @DynamicClassAttribute
    def value(self) -> int:
        """This method overwrite super method for type hint."""
        return super().value


# Since mypy reports following error
# when create "Base" class dynamically from declarative_base() function:
#   Variable "zaimcsvconverter.models.Base" is not valid as a type
# see:
# - Mypy / Pep-484 Support for ORM Mappings — SQLAlchemy 1.4 Documentation
#   https://docs.sqlalchemy.org/en/14/orm/extensions/mypy.html#what-the-plugin-does
# - pep484 Type annotations ,mypy compatibility · Issue #4609 · sqlalchemy/sqlalchemy
#   https://github.com/sqlalchemy/sqlalchemy/issues/4609#issuecomment-782720150
# Reason: Abstract class.
# pylint: disable=too-few-public-methods
class Base(metaclass=DeclarativeMeta):
    __abstract__ = True
    registry = registry()
    metadata = registry.metadata


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


class ConvertTableRecordMixin(Generic[TypeVarBase, TypeVarConvertTableRowData]):
    """This class implements convert table mixin.

    @see https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
    """

    @declared_attr
    # Reason: Since this is class method.
    # see:
    # - Mixin and Custom Base Classes — SQLAlchemy 1.3 Documentation
    #   https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
    # pylint: disable=no-self-argument
    def __tablename__(cls) -> str:
        # Reason: The mypy doesn't check @declared_attr.
        class_name = cls.__name__  # type: ignore
        return str(Inflector().pluralize(class_name.lower()))

    id = Column(Integer, primary_key=True)
    file_csv_convert_id = Column(Integer)
    name = Column(String(255))
    category_payment_large = Column(String(255))
    category_payment_small = Column(String(255))

    __table_args__ = (UniqueConstraint("file_csv_convert_id", "name", name="_name_on_each_account_uc"),)

    @abstractmethod
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: TypeVarConvertTableRowData):
        # Reason: The mypy reports following error:
        #   Attribute "****" already defined on line **
        # see:
        # - Constructors and Object Initialization — SQLAlchemy 1.4 Documentation
        #   https://docs.sqlalchemy.org/en/14/orm/constructors.html
        # - "Already defined" + "not defined" errors with SQLAlchemy 1.2 hybrid_property · Issue #4430 · python/mypy
        #   https://github.com/python/mypy/issues/4430
        self.file_csv_convert_id: int = file_csv_convert_id.value  # type: ignore
        self.name: str = row_data.name  # type: ignore

    @staticmethod
    def _get_str_or_none(value: Optional[str]) -> Optional[str]:
        return value if value != "" else None

    @classmethod
    def try_to_find(cls, file_csv_convert_id: FileCsvConvertId, name: str) -> TypeVarBase:
        """This method select Store model from database.

        If record is not exist, raise NoResultFound.
        """
        try:
            return cls.find(file_csv_convert_id, name)
        except NoResultFound:
            pass
        # ↓ To support Shift JIS
        return cls.find(file_csv_convert_id, name.replace("−", "ー"))

    @classmethod
    def find(cls, file_csv_convert_id: FileCsvConvertId, name: str) -> TypeVarBase:
        """This method select Store model from database."""
        with SessionManager() as session:
            return cast(
                TypeVarBase,
                session.query(cls)
                .filter(cls.file_csv_convert_id == file_csv_convert_id.value, cls.name == name)
                .one(),
            )

    @classmethod
    def save_all(cls, models: List[TypeVarBase]) -> None:
        """This method insert Store models into database."""
        with SessionManager() as session:
            with session.begin():
                session.add_all(models)


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=exc.SAWarning)

    class Store(Base, ConvertTableRecordMixin["Store", StoreRowData]):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        name_zaim = Column(String(255))
        category_income = Column(String(255))
        transfer_target = Column(String(255))

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: StoreRowData):
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            # Reason: The mypy reports following error:
            #   Attribute "****" already defined on line **
            # see:
            # - Constructors and Object Initialization — SQLAlchemy 1.4 Documentation
            #   https://docs.sqlalchemy.org/en/14/orm/constructors.html
            # - "Already defined" + "not defined" errors with SQLAlchemy 1.2 hybrid_property
            #   · Issue #4430 · python/mypy
            #   https://github.com/python/mypy/issues/4430
            self.name_zaim: Optional[str] = self._get_str_or_none(row_data.name_zaim)  # type: ignore
            category_payment_large = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_large: Optional[str] = category_payment_large  # type: ignore
            category_payment_small = self._get_str_or_none(row_data.category_payment_small)
            self.category_payment_small: Optional[str] = category_payment_small  # type: ignore
            self.category_income: Optional[str] = self._get_str_or_none(row_data.category_income)  # type: ignore
            self.transfer_target: Optional[str] = self._get_str_or_none(row_data.transfer_account)  # type: ignore

        @property
        def is_amazon(self) -> bool:
            """This property returns whether this store is Amazon.co.jp or not."""
            return self.name in ["Ａｍａｚｏｎ  Ｄｏｗｎｌｏａｄｓ", "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ", "ＡＭＡＺＯＮ．ＣＯ．ＪＰ"]

        @property
        def is_pay_pal(self) -> bool:
            """This property returns whether this store is Amazon.co.jp or not."""
            return self.name in ["ＰａｙＰａｌ決済"] or re.search(r"PAYPAL\s*", self.name) is not None

    class Item(Base, ConvertTableRecordMixin["Item", ItemRowData]):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: ItemRowData):
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            # Reason: The mypy reports following error:
            #   Attribute "****" already defined on line **
            # see:
            # - Constructors and Object Initialization — SQLAlchemy 1.4 Documentation
            #   https://docs.sqlalchemy.org/en/14/orm/constructors.html
            # - "Already defined" + "not defined" errors with SQLAlchemy 1.2 hybrid_property
            #   · Issue #4430 · python/mypy
            #   https://github.com/python/mypy/issues/4430
            category_payment_large = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_large: Optional[str] = category_payment_large  # type: ignore
            category_payment_small = self._get_str_or_none(row_data.category_payment_small)
            self.category_payment_small: Optional[str] = category_payment_small  # type: ignore


def initialize_database() -> None:
    """This function create empty tables from SQLAlchemy models."""
    # pylint: disable=no-member
    Base.metadata.create_all(Session.get_bind(), checkfirst=False)


@dataclass
class ClassConvertTable(Generic[TypeVarBase, TypeVarConvertTableRowData]):
    """This class implements association of classes about convert table."""

    model: Type[ConvertTableRecordMixin[TypeVarBase, TypeVarConvertTableRowData]]
    row_data: Type[TypeVarConvertTableRowData]


class ConvertTableType(Enum):
    """This class implements types of convert table."""

    STORE = ClassConvertTable(Store, StoreRowData)
    ITEM = ClassConvertTable(Item, ItemRowData)

    @DynamicClassAttribute
    # Reason of Any: Enum class cannot be generic.
    # see:
    #   - Generic versions of enum.Enum? · Issue #535 · python/typing
    #     https://github.com/python/typing/issues/535
    def value(self) -> ClassConvertTable[Any, Any]:
        """This method overwrite super method for type hint."""
        return cast(ClassConvertTable[Any, Any], super().value)
