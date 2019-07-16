"""Tests for mufg.py."""
from datetime import datetime

import pytest

from tests.testlibraries.database import StoreFactory
from tests.conftest import database_session_with_records
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgIncomeRow, MufgPaymentRow, MufgTransferIncomeRow, \
    MufgTransferPaymentRow, MufgRowFactory
from zaimcsvconverter.models import StoreRowData, Store
from zaimcsvconverter.zaim_row import ZaimTransferRow, ZaimIncomeRow, ZaimPaymentRow


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
        assert mufg_row_data.payed_amount == payed_amount
        assert mufg_row_data.deposit_amount == deposit_amount
        assert mufg_row_data.balance == balance
        assert mufg_row_data.note == note
        assert mufg_row_data.is_uncapitalized == is_uncapitalized
        assert mufg_row_data.cash_flow_kind == cash_flow_kind
        assert mufg_row_data.date == datetime(2018, 11, 28, 0, 0)
        assert mufg_row_data.store_name == summary_content


@pytest.fixture
def database_session_stores():
    """This fixture prepares database session and records."""
    def fixture_records():
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('', '', '', '', '', ''),
        )
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('スーパーフツウ', '三菱UFJ銀行', 'その他', 'その他', '臨時収入', ''),
        )
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('トウキヨウトスイドウ', '東京都水道局　経理部管理課', '水道・光熱', '水道料金', '立替金返済', ''),
        )
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('ＧＰマーケテイング', '', '', '', '', 'ゴールドポイントカード・プラス'),
        )
        StoreFactory(
            account=Account.MUFG,
            row_data=StoreRowData('フリコミモト－アカウント', 'フリコミモト－アカウント', '', '', '臨時収入', ''),
        )
    yield from database_session_with_records(fixture_records)


class TestMufgIncomeRow:
    """Tests for MufgIncomeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores):
        """Arguments should set into properties."""
        expected_amount = 10000
        config_account_name = '三菱UFJ銀行'
        config_transfer_account_name = 'お財布'
        mufg_row = MufgIncomeRow(Account.MUFG,
                                 MufgRowData('2018/10/1', 'カ－ド', '', '', '10000', '3000000', '', '', '入金'))
        assert mufg_row.zaim_date == datetime(2018, 10, 1, 0, 0, 0)
        assert isinstance(mufg_row.zaim_store, Store)
        assert mufg_row.zaim_store.name_zaim is None
        assert mufg_row.zaim_income_cash_flow_target == config_account_name
        assert mufg_row.zaim_income_ammount_income == expected_amount
        assert mufg_row.zaim_payment_cash_flow_source == config_transfer_account_name
        assert mufg_row.zaim_payment_note == ''
        assert mufg_row.zaim_payment_amount_payment == expected_amount
        assert mufg_row.zaim_transfer_cash_flow_source == config_transfer_account_name
        assert mufg_row.zaim_transfer_cash_flow_target == config_account_name
        assert mufg_row.zaim_transfer_amount_transfer == expected_amount

    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (MufgRowData('2018/10/1', 'カ－ド', '', '', '10000', '3000000', '', '',	'入金'),
         ZaimTransferRow),
        (MufgRowData('2018/10/1', '振込９', 'フリコミモト－アカウント', '', '10000', '3000000', '', '',	'入金'),
         ZaimIncomeRow),
    ])
    def test_zaim_row_class_to_convert(argument, expected, yaml_config_load, database_session_stores):
        """MufgTransferPaymentRow should convert to ZaimTransferRow."""
        mufg_row = MufgIncomeRow(Account.MUFG, argument)
        validated_input_row = mufg_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == expected


class TestMufgPaymentRow:
    """Tests for MufgPaymentRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores):
        """Arguments should set into properties."""
        mufg_row = MufgPaymentRow(Account.MUFG,
                                  MufgRowData('2018/11/5', 'カ－ド', '', '9000', '', '4000000', '', '', '支払い'))
        expected_amount = 9000
        config_account_name = '三菱UFJ銀行'
        config_transfer_account_name = 'お財布'
        assert mufg_row.zaim_date == datetime(2018, 11, 5, 0, 0, 0)
        assert isinstance(mufg_row.zaim_store, Store)
        assert mufg_row.zaim_store.name_zaim is None
        assert mufg_row.zaim_income_cash_flow_target == config_transfer_account_name
        assert mufg_row.zaim_income_ammount_income == expected_amount
        assert mufg_row.zaim_payment_cash_flow_source == config_account_name
        assert mufg_row.zaim_payment_note == ''
        assert mufg_row.zaim_payment_amount_payment == expected_amount
        assert mufg_row.zaim_transfer_cash_flow_source == config_account_name
        assert mufg_row.zaim_transfer_cash_flow_target == config_transfer_account_name
        assert mufg_row.zaim_transfer_amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    def test_zaim_row_class_to_convert(yaml_config_load, database_session_stores):
        """MufgPaymentRow should convert to ZaimTransferRow."""
        mufg_row = MufgPaymentRow(Account.MUFG,
                                  MufgRowData('2018/11/5', 'カ－ド', '', '9000', '', '4000000', '', '', '支払い'))
        validated_input_row = mufg_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == ZaimTransferRow


class TestMufgTransferIncomeRow:
    """Tests for MufgTransferIncomeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores):
        """Arguments should set into properties."""
        expected_amount = 20
        transfer_target = '三菱UFJ銀行'
        store_name = '三菱UFJ銀行'
        mufg_row = MufgTransferIncomeRow(Account.MUFG,
                                         MufgRowData('2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金'))
        assert mufg_row.zaim_date == datetime(2018, 8, 20, 0, 0, 0)
        assert isinstance(mufg_row.zaim_store, Store)
        assert mufg_row.zaim_store.name_zaim == store_name
        assert mufg_row.zaim_income_cash_flow_target == transfer_target
        assert mufg_row.zaim_income_ammount_income == expected_amount
        assert mufg_row.zaim_payment_cash_flow_source is None
        assert mufg_row.zaim_payment_note == ''
        assert mufg_row.zaim_payment_amount_payment == expected_amount
        assert mufg_row.zaim_transfer_cash_flow_source is None
        assert mufg_row.zaim_transfer_cash_flow_target == transfer_target
        assert mufg_row.zaim_transfer_amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (MufgRowData('2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金'), ZaimIncomeRow),
        (MufgRowData('2018/10/29', '口座振替３', 'ＧＰマ−ケテイング', '', '59260', '3000000', '', '', '振替支払い'), ZaimTransferRow),
    ])
    def test_zaim_row_class_to_convert(argument, expected, yaml_config_load, database_session_stores):
        """MufgTransferIncomeRow should convert to suitable ZaimRow by transfer target."""
        mufg_row = MufgTransferIncomeRow(Account.MUFG, argument)
        validated_input_row = mufg_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == expected


class TestMufgTransferPaymentRow:
    """Tests for MufgTransferPaymentRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init(yaml_config_load, database_session_stores):
        """Arguments should set into properties."""
        expected_amount = 3628
        config_account_name = '三菱UFJ銀行'
        transfer_target = None
        store_name = '東京都水道局　経理部管理課'
        mufg_row = MufgTransferPaymentRow(Account.MUFG,
                                          MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '',
                                                      '振替支払い'))
        assert mufg_row.zaim_date == datetime(2018, 11, 28, 0, 0, 0)
        assert isinstance(mufg_row.zaim_store, Store)
        assert mufg_row.zaim_store.name_zaim == store_name
        assert mufg_row.zaim_income_cash_flow_target == transfer_target
        assert mufg_row.zaim_income_ammount_income == expected_amount
        assert mufg_row.zaim_payment_cash_flow_source == config_account_name
        assert mufg_row.zaim_payment_note == ''
        assert mufg_row.zaim_payment_amount_payment == expected_amount
        assert mufg_row.zaim_transfer_cash_flow_source == config_account_name
        assert mufg_row.zaim_transfer_cash_flow_target == transfer_target
        assert mufg_row.zaim_transfer_amount_transfer == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '振替支払い'), ZaimPaymentRow),
    ])
    def test_zaim_row_class_to_convert(argument, expected, yaml_config_load, database_session_stores):
        """MufgTransferPaymentRow should convert to suitable ZaimRow by transfer target."""
        mufg_row = MufgTransferPaymentRow(Account.MUFG, argument)
        validated_input_row = mufg_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == expected


class TestMufgRowFactory:
    """Tests for MufgRowFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (MufgRowData('2018/10/1', 'カ－ド', '', '', '10000', '3000000', '', '',	'入金'),
         MufgIncomeRow),
        (MufgRowData('2018/11/5', 'カ－ド', '', '9000', '', '4000000', '', '', '支払い'),
         MufgPaymentRow),
        (MufgRowData('2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金'),
         MufgTransferIncomeRow),
        (MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '振替支払い'),
         MufgTransferPaymentRow),
    ])
    def test_create_success(argument, expected, database_session_stores):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        mufg_row = MufgRowFactory().create(Account.MUFG, argument)
        assert isinstance(mufg_row, expected)

    # pylint: disable=unused-argument
    @staticmethod
    def test_create_fail(database_session_stores):
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValueError):
            # pylint: disable=protected-access
            MufgRowFactory().create(
                Account.MUFG,
                MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '')
            )
