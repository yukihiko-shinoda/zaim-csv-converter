"""Tests for model."""
from typing import Optional

import pytest
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session as SQLAlchemySession

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.models import FileCsvConvertId, Store, StoreRowData


class TestModel:
    """Tests for Model."""

    @staticmethod
    def test_save_all(database_session_with_schema: SQLAlchemySession) -> None:
        """Arguments should insert into database."""
        stores = [Store(FileCsvConvertId.WAON, StoreRowData("上尾", "イオンモール　上尾"))]
        Store.save_all(stores)
        store = database_session_with_schema.query(Store).filter(Store.name == "上尾").one()
        assert store.name == "上尾"
        assert store.name_zaim == "イオンモール　上尾"

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        (
            "database_session_with_schema, "
            "file_csv_convert, "
            "store_name, "
            "expected_store_name_zaim, "
            "expected_transfer_target"
        ),
        [
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_MAKUHARISHINTOSHIN],
                FileCsvConvert.WAON,
                "幕張新都心",
                "イオンモール　幕張新都心",
                None,
            ),
            ([InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOBU_CARD], FileCsvConvert.MUFG, "カ）トウブカ－ドビ", None, "東武カード"),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("database_session_with_schema")
    def test_try_to_find_success(
        file_csv_convert: FileCsvConvert,
        store_name: str,
        expected_store_name_zaim: Optional[str],
        expected_transfer_target: Optional[str],
    ) -> None:
        """Method should return Store model when store name is exist in database."""
        store = Store.try_to_find(file_csv_convert.value.id, store_name)
        assert store.name == store_name
        assert store.name_zaim == expected_store_name_zaim
        assert store.transfer_target == expected_transfer_target

    @staticmethod
    @pytest.mark.usefixtures("database_session_with_schema")
    def test_try_to_find_failure() -> None:
        """Method should raise KeyError when store name is not exist in database."""
        with pytest.raises(NoResultFound) as error:
            Store.try_to_find(FileCsvConvert.WAON.value.id, "上尾")
        assert str(error) == "<ExceptionInfo NoResultFound('No row was found when one was required') tblen=6>"
