"""This module implements SQLAlchemy database models."""

from __future__ import annotations

import re
import warnings
from abc import abstractmethod
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from types import DynamicClassAttribute
from typing import Any
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import cast

from inflector import Inflector
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import exc
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.decl_api import registry

from zaimcsvconverter import Session


class FileCsvConvertId(Enum):
    """This class implements file for CSV convert id on database."""

    WAON = 1
    GOLD_POINT_CARD_PLUS = 2
    MUFG = 3
    SF_CARD_VIEWER = 4
    AMAZON = 5
    VIEW_CARD = 6
    PAY_PAL = 7
    SBI_SUMISHIN_NET_BANK = 8
    PAY_PAY_CARD = 9
    MOBILE_SUICA = 10

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

    name_zaim: str | None = None
    category_payment_large: str | None = None
    category_payment_small: str | None = None
    category_income: str | None = None
    transfer_account: str | None = None


@dataclass
class ItemRowData(ConvertTableRowData):
    """This class implements data class for wrapping list of item and category row model."""

    category_payment_large: str | None = None
    category_payment_small: str | None = None


TypeVarConvertTableRowData = TypeVar("TypeVarConvertTableRowData", bound=ConvertTableRowData)


@declarative_mixin
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
    def __tablename__(cls) -> Mapped[str]:  # noqa: N805
        class_name = cls.__class__.__name__
        return mapped_column(str(Inflector().pluralize(class_name.lower())))

    id = mapped_column(Integer, primary_key=True)
    file_csv_convert_id = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255))
    # Reason: SQLAlchemy's bug:
    # - support Mapped[str | None] on Python 3.9 (currently seems not possible) · Issue #9110 · sqlalchemy/sqlalchemy
    #   https://github.com/sqlalchemy/sqlalchemy/issues/9110
    category_payment_large: Mapped[Optional[str]] = mapped_column(String(255))  # noqa: UP007
    category_payment_small: Mapped[Optional[str]] = mapped_column(String(255))  # noqa: UP007

    __table_args__ = (UniqueConstraint("file_csv_convert_id", "name", name="_name_on_each_account_uc"),)

    @abstractmethod
    def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: TypeVarConvertTableRowData) -> None:
        self.file_csv_convert_id = file_csv_convert_id.value
        self.name = row_data.name

    @staticmethod
    def _get_str_or_none(value: str | None) -> str | None:
        return value if value else None

    @classmethod
    def try_to_find(cls, file_csv_convert_id: FileCsvConvertId, name: str) -> TypeVarBase:
        """This method select Store model from database.

        If record is not exist, raise NoResultFound.
        """
        with suppress(NoResultFound):
            return cls.find(file_csv_convert_id, name)
        # ↓ To support Shift JIS. Reason: Specification.
        return cls.find(file_csv_convert_id, name.replace("−", "ー"))  # noqa: RUF001

    @classmethod
    def find(cls, file_csv_convert_id: FileCsvConvertId, name: str) -> TypeVarBase:
        """This method select Store model from database."""
        with Session() as session:
            return cast(
                "TypeVarBase",
                session.execute(
                    select(cls).where(cls.file_csv_convert_id == file_csv_convert_id.value, cls.name == name),
                ).scalar_one(),
            )

    @classmethod
    def save_all(cls, models: list[TypeVarBase]) -> None:
        """This method insert Store models into database."""
        with Session() as session:
            session.add_all(models)
            session.commit()


with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=exc.SAWarning)

    class Store(Base, ConvertTableRecordMixin["Store", StoreRowData]):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        # The types are by default always considered to be Optional,
        # even for the primary key and non-nullable column.
        # The types of the above columns can be stated explicitly,
        # providing the two advantages of clearer self-documentation
        # as well as being able to control which types are optional.
        # - Mypy / Pep-484 Support for ORM Mappings — SQLAlchemy 1.4 Documentation
        #   https://docs.sqlalchemy.org/en/14/orm/extensions/mypy.html#introspection-of-columns-based-on-typeengine
        # Reason: SQLAlchemy's bug:
        # - support Mapped[str | None] on Python 3.9 (currently seems not possible) · Issue #9110 · sqlalchemy/sqlalchemy pylint: disable=line-too-long
        #   https://github.com/sqlalchemy/sqlalchemy/issues/9110
        name_zaim: Mapped[Optional[str]] = mapped_column(String(255))  # noqa: UP007
        category_income: Mapped[Optional[str]] = mapped_column(String(255))  # noqa: UP007
        transfer_target: Mapped[Optional[str]] = mapped_column(String(255))  # noqa: UP007

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: StoreRowData) -> None:
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            self.name_zaim = self._get_str_or_none(row_data.name_zaim)
            category_payment_large = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_large = category_payment_large
            category_payment_small = self._get_str_or_none(row_data.category_payment_small)
            self.category_payment_small = category_payment_small
            self.category_income = self._get_str_or_none(row_data.category_income)
            self.transfer_target = self._get_str_or_none(row_data.transfer_account)

        @property
        def is_amazon(self) -> bool:
            """This property returns whether this store is Amazon.co.jp or not."""
            # Reason: Specification.
            return self.name in [
                "Ａｍａｚｏｎ  Ｄｏｗｎｌｏａｄｓ",  # noqa: RUF001
                "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ",  # noqa: RUF001
                "ＡＭＡＺＯＮ．ＣＯ．ＪＰ",  # noqa: RUF001
            ]

        @property
        def is_pay_pal(self) -> bool:
            """This property returns whether this store is PayPal or not."""
            # Reason: Specification.
            return self.name in ["ＰａｙＰａｌ決済"] or (
                self.name is not None and re.search(r"PAYPAL\s*", self.name) is not None
            )

        @property
        def is_kyash(self) -> bool:
            """This property returns whether this store is Kyash or not."""
            # Reason: Specification.
            return bool(self.name == "ＫＹＡＳＨ")  # noqa: RUF001

    class Item(Base, ConvertTableRecordMixin["Item", ItemRowData]):
        """This class implements Store model to convert from account CSV to Zaim CSV."""

        def __init__(self, file_csv_convert_id: FileCsvConvertId, row_data: ItemRowData) -> None:
            ConvertTableRecordMixin.__init__(self, file_csv_convert_id, row_data)
            category_payment_large = self._get_str_or_none(row_data.category_payment_large)
            self.category_payment_large = category_payment_large
            category_payment_small = self._get_str_or_none(row_data.category_payment_small)
            self.category_payment_small = category_payment_small


def initialize_database() -> None:
    """This function create empty tables from SQLAlchemy models."""
    # pylint: disable=no-member
    Base.metadata.create_all(Session.get_bind(), checkfirst=False)


@dataclass
class ClassConvertTable(Generic[TypeVarBase, TypeVarConvertTableRowData]):
    """This class implements association of classes about convert table."""

    model: type[ConvertTableRecordMixin[TypeVarBase, TypeVarConvertTableRowData]]
    row_data: type[TypeVarConvertTableRowData]


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
        return cast("ClassConvertTable[Any, Any]", super().value)
