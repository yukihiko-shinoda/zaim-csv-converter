"""This module implements testing utility using SQLAlchemy and factory_boy.

@see https://factoryboy.readthedocs.io/en/latest/orms.html#sqlalchemy
"""

from collections.abc import Generator
from dataclasses import dataclass
from typing import Optional

import factory
from sqlalchemy.orm.session import Session as SQLAlchemySession

from tests.testlibraries.database_engine_manager import DatabaseEngineManager
from zaimcsvconverter.models import Base, ConvertTableRowData, FileCsvConvertId, Item, Store
from zaimcsvconverter import Session


class StoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Store model."""

    class Meta:  # Reason: Model. pylint: disable=too-few-public-methods
        """Settings for factory_boy."""

        model = Store
        sqlalchemy_session = Session


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Store model."""

    class Meta:  # Reason: Model. pylint: disable=too-few-public-methods
        """Settings for factory_boy."""

        model = Item
        sqlalchemy_session = Session


@dataclass
class FixtureRecord:
    """This class implements properties and method to define factory_boy fixture records."""

    file_csv_convert_id: FileCsvConvertId
    row_data: ConvertTableRowData

    def define(self) -> None:
        """This method defines factory_boy fixture records by using properties."""
        if self.file_csv_convert_id is FileCsvConvertId.AMAZON:
            # Reason: Mypy and SQLAlchemy's issue
            ItemFactory(file_csv_convert_id=self.file_csv_convert_id, row_data=self.row_data)  # type: ignore[no-untyped-call]  # noqa: E501 RUF100 pylint: disable=line-too-long
        elif self.file_csv_convert_id in (
            FileCsvConvertId.WAON,
            FileCsvConvertId.GOLD_POINT_CARD_PLUS,
            FileCsvConvertId.MUFG,
            FileCsvConvertId.SF_CARD_VIEWER,
            FileCsvConvertId.VIEW_CARD,
        ):
            # Reason: Mypy and SQLAlchemy's issue
            StoreFactory(file_csv_convert_id=self.file_csv_convert_id, row_data=self.row_data)  # type: ignore[no-untyped-call]  # noqa: E501 RUF100 pylint: disable=line-too-long
        else:
            msg = (
                "self.file_csv_convert_id is not supported on this class. "
                f"self.file_csv_convert_id = {self.file_csv_convert_id}"
            )
            raise ValueError(msg)


class DatabaseForTest:
    """This class implements methods about database for unit testing."""

    @classmethod
    def database_session(cls) -> Generator[SQLAlchemySession, None, None]:
        """This fixture prepares database session to reset database after each test."""
        with DatabaseEngineManager(Session):
            yield Session()

    @classmethod
    def database_session_with_schema(
        cls,
        list_fixture_record: Optional[list[FixtureRecord]] = None,
    ) -> Generator[SQLAlchemySession, None, None]:
        """This fixture prepares database session and fixture records to reset database after each test."""
        with DatabaseEngineManager(Session) as engine:
            session = Session()
            Base.metadata.create_all(engine)
            if list_fixture_record is not None:
                for fixture_record in list_fixture_record:
                    fixture_record.define()
            session.commit()
            yield session
