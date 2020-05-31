"""Tests for mufg.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.mufg import (
    MufgIncomeFromOthersRow,
    MufgIncomeRow,
    MufgPaymentRow,
    MufgPaymentToSomeoneRow,
    MufgRowData,
    MufgRowFactory,
)
from zaimcsvconverter.rowconverters.mufg import (
    MufgIncomeZaimTransferRowConverter,
    MufgPaymentZaimTransferRowConverter,
    MufgTransferIncomeZaimTransferRowConverter,
    MufgTransferPaymentZaimTransferRowConverter,
    MufgZaimIncomeRowConverter,
    MufgZaimPaymentRowConverter,
    MufgZaimRowConverterFactory,
)
from zaimcsvconverter.zaim_row import ZaimIncomeRow, ZaimPaymentRow, ZaimRowFactory, ZaimTransferRow


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
    def test(
        mufg_row_data: MufgRowData,
        expected_date,
        expected_store,
        config_transfer_account_name,
        expect_cash_flow_target,
        expected_amount,
        yaml_config_load,
        database_session_stores_mufg,
    ):
        """Arguments should set into properties."""
        mufg_row = MufgIncomeFromOthersRow(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(MufgZaimIncomeRowConverter(mufg_row))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)  # type: ignore
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_target == expect_cash_flow_target
        assert zaim_row_data.amount_income == expected_amount


class TestMufgZaimPaymentRowConverter:
    """Tests for MufgZaimPaymentRowConverter."""

    # pylint: disable=unused-argument
    @staticmethod
    def test(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        expected_amount = 3628
        config_account_name = "三菱UFJ銀行"
        store_name = "東京都水道局　経理部管理課"
        mufg_row = MufgPaymentToSomeoneRow(InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(MufgZaimPaymentRowConverter(mufg_row))
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
    def test_input_row(
        mufg_row_data,
        expected_date,
        config_transfer_account_name,
        config_account_name,
        expected_amount,
        yaml_config_load,
        database_session_stores_mufg,
    ):
        """Arguments should set into properties."""
        mufg_row = MufgIncomeRow(mufg_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(MufgIncomeZaimTransferRowConverter(mufg_row))
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
    def test_payment_row(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        expected_amount = 9000
        config_account_name = "三菱UFJ銀行"
        config_transfer_account_name = "お財布"
        # Reason: Pylint's bug. pylint: disable=no-member
        mufg_row = MufgPaymentRow(InstanceResource.ROW_DATA_MUFG_PAYMENT)
        zaim_row = ZaimRowFactory.create(MufgPaymentZaimTransferRowConverter(mufg_row))
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
    def test_transfer_income_row(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        expected_amount = 20
        transfer_target = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        mufg_row = MufgIncomeFromOthersRow(InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT)
        zaim_row = ZaimRowFactory.create(MufgTransferIncomeZaimTransferRowConverter(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-08-20"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source is None
        assert zaim_row_data.cash_flow_target == transfer_target
        assert zaim_row_data.amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    def test_transfer_payment_row(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        expected_amount = 3628
        config_account_name = "三菱UFJ銀行"
        # Reason: Pylint's bug. pylint: disable=no-member
        mufg_row = MufgPaymentToSomeoneRow(InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS)
        zaim_row = ZaimRowFactory.create(MufgTransferPaymentZaimTransferRowConverter(mufg_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-28"
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == config_account_name
        assert zaim_row_data.cash_flow_target is None
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
    def test_success(yaml_config_load, database_session_with_schema, input_row_data: MufgRowData, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = MufgRowFactory().create(input_row_data)
        assert isinstance(MufgZaimRowConverterFactory().create(input_row), expected)
