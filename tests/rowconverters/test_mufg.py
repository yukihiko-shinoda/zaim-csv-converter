"""Tests for mufg.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.csvconverter.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputcsvformats import InputRow, InputRowData
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData
from zaimcsvconverter.rowconverters.mufg import (
    MufgIncomeZaimTransferRowConverter,
    MufgPaymentZaimTransferRowConverter,
    MufgTransferIncomeZaimTransferRowConverter,
    MufgTransferPaymentZaimTransferRowConverter,
    MufgZaimIncomeRowConverter,
    MufgZaimPaymentRowConverter,
)
from zaimcsvconverter.rowconverters import ZaimRowConverter
from zaimcsvconverter.zaim.zaim_row import ZaimIncomeRow, ZaimPaymentRow, ZaimRowFactory, ZaimTransferRow


class TestMufgZaimIncomeRowConverter:
    """Tests for MufgZaimIncomeRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            "mufg_row_data, expected_date, expected_store, config_transfer_account_name, expect_cash_flow_target, "
            "expected_amount"
        ),
        [
            #  1. income and not by card
            (InstanceResource.ROW_DATA_MUFG_INCOME_NOT_CARD, "2018-10-01", "フリコミモト－アカウント", "お財布", "三菱UFJ銀行", 10000),
            #  2. transfer and not defined transfer target on convert table
            (
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT,
                "2018-08-20",
                "三菱UFJ銀行",
                None,
                "三菱UFJ銀行",
                20,
            ),
        ],
    )
    @pytest.mark.usefixtures("config_transfer_account_name", "yaml_config_load", "database_session_stores_mufg")
    def test(
        mufg_row_data: MufgRowData,
        expected_date: str,
        expected_store: str,
        expect_cash_flow_target: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_target == expect_cash_flow_target
        assert zaim_row_data.amount_income == expected_amount


class TestMufgZaimPaymentRowConverter:
    """Tests for MufgZaimPaymentRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 3628
        config_account_name = "三菱UFJ銀行"
        store_name = "東京都水道局　経理部管理課"
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS
        )
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-28"
        assert zaim_row_data.store_name == store_name
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.note == ""
        assert zaim_row_data.amount_payment == expected_amount


class TestMufgZaimTransferRowConverter:
    """Tests for MufgZaimTransferRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "mufg_row_data, expected_date, config_transfer_account_name, config_account_name, expected_amount",
        [(InstanceResource.ROW_DATA_MUFG_INCOME_CARD, "2018-10-01", "お財布", "三菱UFJ銀行", 10000)],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_input_row(
        mufg_row_data: MufgRowData,
        expected_date: str,
        config_transfer_account_name: str,
        config_account_name: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_transfer_account_name
        assert zaim_row_data.cash_flow_target == config_account_name
        assert zaim_row_data.amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_payment_row() -> None:
        """Arguments should set into properties."""
        expected_amount = 9000
        config_account_name = "三菱UFJ銀行"
        config_transfer_account_name = "お財布"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(InstanceResource.ROW_DATA_MUFG_PAYMENT)
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-05"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.cash_flow_target == config_transfer_account_name
        assert zaim_row_data.amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_transfer_income_row() -> None:
        """Arguments should set into properties."""
        expected_amount = 10000
        transfer_target = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_OWN_ACCOUNT
        )
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-10-20"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == "お財布"
        assert zaim_row_data.cash_flow_target == transfer_target
        assert zaim_row_data.amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_transfer_payment_row() -> None:
        """Arguments should set into properties."""
        expected_amount = 59260
        config_account_name = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_GOLD_POINT_MARKETING
        )
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-10-29"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.cash_flow_target == "ゴールドポイントカード・プラス"
        assert zaim_row_data.amount_transfer == expected_amount


class TestMufgZaimRowConverterFactory:
    """Tests for MufgZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when MUFG income by card
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY],
                InstanceResource.ROW_DATA_MUFG_INCOME_CARD,
                MufgIncomeZaimTransferRowConverter,
            ),
            # Case when MUFG income not by card
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_OTHER_ACCOUNT],
                InstanceResource.ROW_DATA_MUFG_INCOME_NOT_CARD,
                MufgZaimIncomeRowConverter,
            ),
            # Case when MUFG payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY],
                InstanceResource.ROW_DATA_MUFG_PAYMENT,
                MufgPaymentZaimTransferRowConverter,
            ),
            # Case when MUFG transfer income which transfer_target doesn't exist
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG],
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT,
                MufgZaimIncomeRowConverter,
            ),
            # Case when MUFG transfer income which transfer_target exists
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG_TRUST_AND_BANK],
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_OWN_ACCOUNT,
                MufgTransferIncomeZaimTransferRowConverter,
            ),
            # Case when MUFG transfer payment which transfer_target doesn't exist
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOKYO_WATERWORKS],
                InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS,
                MufgZaimPaymentRowConverter,
            ),
            # Case when MUFG transfer payment transfer_target exists
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_GOLD_POINT_MARKETING],
                InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_GOLD_POINT_MARKETING,
                MufgTransferPaymentZaimTransferRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_success(
        input_row_data: MufgRowData,
        expected: type[ZaimRowConverter[InputRow[InputRowData], InputRowData]],
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        input_row = csv_record_processor.create_input_row_instance(input_row_data)
        actual = account_context.zaim_row_converter_factory.create(input_row)
        assert isinstance(actual, expected)
