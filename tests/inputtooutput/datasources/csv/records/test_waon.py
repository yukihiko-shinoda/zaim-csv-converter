"""Tests for waon.py."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonChargeRow, WaonRow, WaonRowToSkip
from zaimcsvconverter.models import Store


class TestWaonRow:
    """Tests for WaonRow."""

    # pylint: disable=too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("waon_row_data", "expected_date", "expected_store_name_zaim", "expected_amount"),
        [
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                # Reason: Time is not used in this process.
                datetime(2018, 8, 7, 0, 0, 0),  # noqa: DTZ001
                "ファミリーマート　かぶと町永代通り店",
                129,
            ),
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
                # Reason: Time is not used in this process.
                datetime(2018, 8, 30, 0, 0, 0),  # noqa: DTZ001
                "イオンスタイル　板橋前野町",
                1489,
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test_init_success(
        waon_row_data: WaonRowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties.

        :param WaonRowData waon_row_data:
        """
        waon_row = WaonRow(waon_row_data)
        assert waon_row.date == expected_date
        assert isinstance(waon_row.store, Store)
        assert waon_row.store.name_zaim == expected_store_name_zaim
        assert waon_row.used_amount == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_basic_store_waon")
    def test_is_row_to_skip() -> None:
        """WaonRow which express download point should be row to skip."""
        waon_row_data_factory = RowDataFactory(WaonRowData)
        assert WaonRowToSkip(
            waon_row_data_factory.create(["2018/10/22", "板橋前野町", "0円", "ポイントダウンロード", "-"]),
        ).is_row_to_skip
        assert WaonRowToSkip(
            waon_row_data_factory.create(
                [
                    "2020/10/23",
                    "イオン銀行ＭＳ板橋区役所前１",
                    "9,863円",
                    "WAON移行（アップロード）",  # noqa: RUF001
                    "-",
                ],
            ),
        ).is_row_to_skip
        assert WaonRowToSkip(
            waon_row_data_factory.create(
                [
                    "2020/10/23",
                    "イオン銀行ＭＳ板橋区役所前１",
                    "9,863円",
                    "WAON移行（ダウンロード）",  # noqa: RUF001
                    "-",
                ],
            ),
        ).is_row_to_skip


class TestWaonChargeRow:
    """Tests for WaonChargeRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_charge_kind_fail() -> None:
        """Property should raise ValueError when charge kind is null on WAON charge row."""
        with pytest.raises(ValueError, match=r"Charge\skind\son\scharge\srow\sis\snot\sallowed\s\"\-\"\."):
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            WaonChargeRow(  # noqa: B018
                InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO,
            ).charge_kind
