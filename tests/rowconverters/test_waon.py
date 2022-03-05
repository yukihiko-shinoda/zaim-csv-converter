"""Tests for waon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputcsvformats import InputRow, InputRowData
from zaimcsvconverter.inputcsvformats.waon import WaonRowData
from zaimcsvconverter.rowconverters.waon import (
    WaonZaimIncomeRowConverter,
    WaonZaimPaymentRowConverter,
    WaonZaimTransferRowConverter,
)
from zaimcsvconverter.rowconverters import ZaimRowConverter
from zaimcsvconverter.zaim.zaim_row import ZaimIncomeRow, ZaimPaymentRow, ZaimRowFactory, ZaimTransferRow


class TestWaonZaimIncomeRowConverter:
    """Tests for WaonZaimIncomeRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "waon_row_data, expected_date, expected_store, expected_amount_income",
        [(InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, "2018-10-22", "イオンスタイル　板橋前野町", 1504)],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test(
        waon_row_data: WaonRowData,
        expected_date: str,
        expected_store: str,
        expected_amount_income: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_target == "WAON"
        assert zaim_row_data.amount_income == expected_amount_income


class TestWaonZaimPaymentRowConverter:
    """Tests for WaonZaimPaymentRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "waon_row_data, expected_date, expected_store, expected_amount_payment",
        [
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                "2018-08-07",
                "ファミリーマート　かぶと町永代通り店",
                129,
            ),
            (InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO, "2018-08-30", "イオンスタイル　板橋前野町", 1489),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test(
        waon_row_data: WaonRowData,
        expected_date: str,
        expected_store: str,
        expected_amount_payment: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == "WAON"
        assert zaim_row_data.amount_payment == expected_amount_payment


class TestWaonZaimTransferRowConverter:
    """Tests for WaonZaimTransferRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "waon_row_data, expected_date, expected_amount_payment",
        [
            # 1. auto charge
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, "2018-11-11", 5000),
            # 2. charge from bank account
            (InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO, "2018-10-22", 10000),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test(waon_row_data: WaonRowData, expected_date: str, expected_amount_payment: int) -> None:
        """Arguments should set into properties."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context)
        waon_row = csv_record_processor.create_input_row_instance(waon_row_data)
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(waon_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.cash_flow_source == "イオン銀行"
        assert zaim_row_data.cash_flow_target == "WAON"
        assert zaim_row_data.amount_transfer == expected_amount_payment


class TestWaonZaimRowConverterConverter:
    """Tests for WaonZaimRowConverterConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when WAON payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI],
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                WaonZaimPaymentRowConverter,
            ),
            # Case when WAON charge from point
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO,
                WaonZaimIncomeRowConverter,
            ),
            # Case when WAON auto charge
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON charge by bank account
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON charge by cash
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                InstanceResource.ROW_DATA_WAON_CHARGE_CASH_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON charge by value download
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                InstanceResource.ROW_DATA_WAON_CHARGE_DOWNLOAD_VALUE_ITABASHIMAENOCHO,
                WaonZaimIncomeRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_success(
        input_row_data: WaonRowData,
        expected: type[ZaimRowConverter[InputRow[InputRowData], InputRowData]],
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context)
        input_row = csv_record_processor.create_input_row_instance(input_row_data)
        actual = account_context.zaim_row_converter_factory.create(input_row)
        assert isinstance(actual, expected)

    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_fail() -> None:
        """Create method should raise ValueError when input row is undefined type."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context)
        input_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO
        )
        with pytest.raises(ValueError) as error:
            account_context.zaim_row_converter_factory.create(input_row)
        assert str(error.value) == "Unsupported row. Input row = WaonRow, ポイントダウンロード"
