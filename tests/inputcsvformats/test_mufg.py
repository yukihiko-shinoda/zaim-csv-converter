"""Tests for mufg.py."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgRowFactory, MufgStoreRow, MufgRow
from zaimcsvconverter.models import Store, AccountId


class TestMufgRowData:
    """Tests for MufgRowData."""

    @staticmethod
    def test_init_and_property():
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        date = '2018/11/28'
        summary = '水道'
        summary_content = 'トウキヨウトスイドウ'
        payed_amount = '3628'
        deposit_amount = ''
        balance = '5000000'
        note = ''
        is_uncapitalized = ''
        cash_flow_kind = '振替支払い'
        mufg_row_data = MufgRowData(date, summary, summary_content, payed_amount, deposit_amount, balance, note,
                                    is_uncapitalized, cash_flow_kind)
        assert mufg_row_data.summary == summary
        assert mufg_row_data.payed_amount == 3628
        assert mufg_row_data.deposit_amount is None
        assert mufg_row_data.balance == balance
        assert mufg_row_data.note == note
        assert mufg_row_data.is_uncapitalized == is_uncapitalized
        assert mufg_row_data.cash_flow_kind == MufgRowData.CashFlowKind.TRANSFER_PAYMENT
        assert mufg_row_data.date == datetime(2018, 11, 28, 0, 0)
        assert mufg_row_data.store_name == summary_content


class TestMufgIncomeRow:
    """Tests for MufgIncomeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        mufg_row = MufgStoreRow(AccountId.MUFG, InstanceResource.ROW_DATA_MUFG_INCOME_CARD)
        assert mufg_row.date == datetime(2018, 10, 1, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim is None


class TestMufgPaymentRow:
    """Tests for MufgPaymentRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        mufg_row = MufgStoreRow(AccountId.MUFG, InstanceResource.ROW_DATA_MUFG_PAYMENT)
        assert mufg_row.date == datetime(2018, 11, 5, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim is None


class TestMufgTransferIncomeRow:
    """Tests for MufgTransferIncomeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        store_name = '三菱UFJ銀行'
        mufg_row = MufgStoreRow(AccountId.MUFG, InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT)
        assert mufg_row.date == datetime(2018, 8, 20, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim == store_name


class TestMufgTransferPaymentRow:
    """Tests for MufgTransferPaymentRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores_mufg):
        """Arguments should set into properties."""
        store_name = '東京都水道局　経理部管理課'
        mufg_row = MufgStoreRow(AccountId.MUFG, InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS)
        assert mufg_row.date == datetime(2018, 11, 28, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim == store_name


class TestMufgRowFactory:
    """Tests for MufgRowFactory."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        'argument, expected_is_income, expected_is_payment, expected_is_transfer_income, expected_is_transfer_payment',
        [
            (InstanceResource.ROW_DATA_MUFG_INCOME_CARD, True, False, False, False),
            (InstanceResource.ROW_DATA_MUFG_PAYMENT, False, True, False, False),
            (InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT, False, False, True, False),
            (InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS, False, False, False, True),
        ]
    )
    def test_create_success(database_session_stores_mufg, argument, expected_is_income, expected_is_payment,
                            expected_is_transfer_income, expected_is_transfer_payment):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        mufg_row = MufgRowFactory().create(AccountId.MUFG, argument)
        assert isinstance(mufg_row, MufgRow)
        assert mufg_row.is_income == expected_is_income
        assert mufg_row.is_payment == expected_is_payment
        assert mufg_row.is_transfer_income == expected_is_transfer_income
        assert mufg_row.is_transfer_payment == expected_is_transfer_payment

    # pylint: disable=unused-argument
    @staticmethod
    def test_create_fail(database_session_stores_mufg):
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValueError):
            # pylint: disable=protected-access
            MufgRowFactory().create(AccountId.MUFG, InstanceResource.ROW_DATA_MUFG_UNSUPPORTED_NOTE)
