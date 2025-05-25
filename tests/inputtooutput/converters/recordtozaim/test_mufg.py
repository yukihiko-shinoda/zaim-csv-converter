"""Tests for mufg.py."""

from pathlib import Path

import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimIncomeRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimTransferRow


class TestMufgZaimIncomeRowConverter:
    """Tests for MufgZaimIncomeRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            "mufg_row_data",
            "expected_date",
            "expected_store",
            "config_transfer_account_name",
            "expect_cash_flow_target",
            "expected_amount",
        ),
        [
            #  1. income and not by card
            (
                InstanceResource.ROW_DATA_MUFG_INCOME_NOT_CARD,
                "2018-10-01",
                "フリコミモト－アカウント",  # noqa: RUF001
                "お財布",
                "三菱UFJ銀行",
                10000,
            ),
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
    @pytest.mark.usefixtures("config_transfer_account_name", "_yaml_config_load", "database_session_stores_mufg")
    def test(
        mufg_row_data: MufgRowData,
        expected_date: str,
        expected_store: str,
        expect_cash_flow_target: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        item_name = ""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [expected_date, expect_cash_flow_target, item_name, expected_store, expected_amount],
            attribute_filter=["date", "cash_flow_target", "item_name", "store_name", "amount_income"],
        )


class TestMufgZaimPaymentRowConverter:
    """Tests for MufgZaimPaymentRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_mufg")
    def test() -> None:
        """Arguments should set into properties."""
        expected_amount = 3628
        config_account_name = "三菱UFJ銀行"
        store_name = "東京都水道局　経理部管理課"
        item_name = ""
        note = ""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS,
        )
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            ["2018-11-28", config_account_name, item_name, note, store_name, expected_amount],
            attribute_filter=["date", "cash_flow_source", "item_name", "note", "store_name", "amount_payment"],
        )


class TestMufgZaimTransferRowConverter:
    """Tests for MufgZaimTransferRowConverter."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("mufg_row_data", "expected_date", "config_transfer_account_name", "config_account_name", "expected_amount"),
        [(InstanceResource.ROW_DATA_MUFG_INCOME_CARD, "2018-10-01", "お財布", "三菱UFJ銀行", 10000)],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_mufg")
    def test_input_row(
        mufg_row_data: MufgRowData,
        expected_date: str,
        config_transfer_account_name: str,
        config_account_name: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        store_name = ""
        item_name = ""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [expected_date, config_transfer_account_name, config_account_name, item_name, store_name, expected_amount],
            attribute_filter=[
                "date",
                "cash_flow_source",
                "cash_flow_target",
                "item_name",
                "store_name",
                "amount_transfer",
            ],
        )

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_mufg")
    def test_payment_row() -> None:
        """Arguments should set into properties."""
        store_name = ""
        item_name = ""
        expected_amount = 9000
        config_account_name = "三菱UFJ銀行"
        config_transfer_account_name = "お財布"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(InstanceResource.ROW_DATA_MUFG_PAYMENT)
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            ["2018-11-05", config_account_name, config_transfer_account_name, item_name, store_name, expected_amount],
            attribute_filter=[
                "date",
                "cash_flow_source",
                "cash_flow_target",
                "item_name",
                "store_name",
                "amount_transfer",
            ],
        )

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_mufg")
    def test_transfer_income_row() -> None:
        """Arguments should set into properties."""
        store_name = ""
        item_name = ""
        expected_amount = 10000
        transfer_target = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_OWN_ACCOUNT,
        )
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            ["2018-10-20", "お財布", transfer_target, item_name, store_name, expected_amount],
            attribute_filter=[
                "date",
                "cash_flow_source",
                "cash_flow_target",
                "item_name",
                "store_name",
                "amount_transfer",
            ],
        )

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_stores_mufg")
    def test_transfer_payment_row() -> None:
        """Arguments should set into properties."""
        store_name = ""
        item_name = ""
        expected_amount = 59260
        config_account_name = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_GOLD_POINT_MARKETING,
        )
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert_each_properties(
            zaim_row_data,
            [
                "2018-10-29",
                config_account_name,
                "ゴールドポイントカード・プラス",
                item_name,
                store_name,
                expected_amount,
            ],
            attribute_filter=[
                "date",
                "cash_flow_source",
                "cash_flow_target",
                "item_name",
                "store_name",
                "amount_transfer",
            ],
        )
