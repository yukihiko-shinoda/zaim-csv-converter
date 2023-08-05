"""Tests for waon.py."""
from pathlib import Path
from typing import cast

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimIncomeRow, ZaimPaymentRow, ZaimTransferRow


class TestWaonZaimIncomeRowConverter:
    """Tests for WaonZaimIncomeRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("waon_row_data", "expected_date", "expected_store", "expected_amount_income"),
        [
            (
                InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO,
                "2018-10-22",
                "イオンスタイル　板橋前野町",
                1504,
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test(
        waon_row_data: WaonRowData,
        expected_date: str,
        expected_store: str,
        expected_amount_income: int,
    ) -> None:
        """Arguments should set into properties."""
        item_name = ""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row, Path()))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [expected_date, "WAON", item_name, expected_store, expected_amount_income],
            attribute_filter=["date", "cash_flow_target", "item_name", "store_name", "amount_income"],
        )


class TestWaonZaimPaymentRowConverter:
    """Tests for WaonZaimPaymentRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("waon_row_data", "expected_date", "expected_store", "expected_amount_payment"),
        [
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                "2018-08-07",
                "ファミリーマート　かぶと町永代通り店",
                129,
            ),
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
                "2018-08-30",
                "イオンスタイル　板橋前野町",
                1489,
            ),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test(
        waon_row_data: WaonRowData,
        expected_date: str,
        expected_store: str,
        expected_amount_payment: int,
    ) -> None:
        """Arguments should set into properties."""
        item_name = ""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row, Path()))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [expected_date, "WAON", item_name, expected_store, expected_amount_payment],
            attribute_filter=["date", "cash_flow_source", "item_name", "store_name", "amount_payment"],
        )


class TestWaonZaimTransferRowConverter:
    """Tests for WaonZaimTransferRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("waon_row_data", "expected_date", "expected_amount_payment"),
        [
            # 1. auto charge
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, "2018-11-11", 5000),
            # 2. charge from bank account
            (InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO, "2018-10-22", 10000),
        ],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_basic_store_waon")
    def test(waon_row_data: WaonRowData, expected_date: str, expected_amount_payment: int) -> None:
        """Arguments should set into properties."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row, Path()))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [expected_date, "イオン銀行", "WAON", expected_amount_payment],
            attribute_filter=["date", "cash_flow_source", "cash_flow_target", "amount_transfer"],
        )


class TestWaonZaimRowConverterConverter:
    """Tests for WaonZaimRowConverterConverter."""

    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_fail(self) -> None:
        """Create method should raise ValueError when input row is undefined type."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        input_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO,
        )
        # Reason: To fix, it is necessary to recreate designs of ZaimRowConverterFactory.
        dekinded_input_row = cast(WaonRow, input_row)
        assert dekinded_input_row.is_row_to_skip
