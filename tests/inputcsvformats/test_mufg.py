#!/usr/bin/env python
"""Tests for mufg.py."""
from datetime import datetime

import unittest2 as unittest
from parameterized import parameterized

from tests.resource import DatabaseTestCase, StoreFactory, ConfigurableDatabaseTestCase
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData, MufgIncomeRow, MufgPaymentRow, MufgTransferIncomeRow, \
    MufgTransferPaymentRow, MufgRowFactory
from zaimcsvconverter.models import StoreRowData, Store


class TestMufgRowData(unittest.TestCase):
    """Tests for MufgRowData."""

    def test_init_and_property(self):
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
        self.assertEqual(mufg_row_data.summary, summary)
        self.assertEqual(mufg_row_data.payed_amount, payed_amount)
        self.assertEqual(mufg_row_data.deposit_amount, deposit_amount)
        self.assertEqual(mufg_row_data.balance, balance)
        self.assertEqual(mufg_row_data.note, note)
        self.assertEqual(mufg_row_data.is_uncapitalized, is_uncapitalized)
        self.assertEqual(mufg_row_data.cash_flow_kind, cash_flow_kind)
        self.assertEqual(mufg_row_data.date, datetime(2018, 11, 28, 0, 0))
        self.assertEqual(mufg_row_data.store_name, summary_content)


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.MUFG,
        row_data=StoreRowData('', '', '', '', '', ''),
    )
    StoreFactory(
        account=Account.MUFG,
        row_data=StoreRowData('スーパーフツウ', '三菱UFJ銀行', 'その他', 'その他', '臨時収入', '三菱UFJ銀行'),
    )
    StoreFactory(
        account=Account.MUFG,
        row_data=StoreRowData('トウキヨウトスイドウ', '東京都水道局　経理部管理課', '水道・光熱', '水道料金', '立替金返済', 'ゴールドポイントカード・プラス'),
    )


class TestMufgIncomeRow(ConfigurableDatabaseTestCase):
    """Tests for MufgIncomeRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """Arguments should set into properties."""
        mufg_row_data = MufgRowData('2018/10/1', 'カ－ド', '', '', '10000', '3000000', '', '',	'入金')
        expected_amount = 10000
        config_account_name = '三菱UFJ銀行'
        config_transfer_account_name = 'お財布'
        mufg_row = MufgIncomeRow(Account.MUFG, mufg_row_data)
        self.assertEqual(mufg_row.zaim_date, datetime(2018, 10, 1, 0, 0, 0))
        self.assertIsInstance(mufg_row.zaim_store, Store)
        self.assertIsNone(mufg_row.zaim_store.name_zaim)
        self.assertEqual(mufg_row.zaim_income_cash_flow_target, config_account_name)
        self.assertEqual(mufg_row.zaim_income_ammount_income, expected_amount)
        self.assertEqual(mufg_row.zaim_payment_cash_flow_source, config_transfer_account_name)
        self.assertEqual(mufg_row.zaim_payment_note, '')
        self.assertEqual(mufg_row.zaim_payment_amount_payment, expected_amount)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_source, config_transfer_account_name)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_target, config_account_name)
        self.assertEqual(mufg_row.zaim_transfer_amount_transfer, expected_amount)


class TestMufgPaymentRow(ConfigurableDatabaseTestCase):
    """Tests for MufgPaymentRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """Arguments should set into properties."""
        mufg_row_data = MufgRowData('2018/11/5', 'カ－ド', '', '9000', '', '4000000', '', '', '支払い')
        expected_amount = 9000
        config_account_name = '三菱UFJ銀行'
        config_transfer_account_name = 'お財布'
        mufg_row = MufgPaymentRow(Account.MUFG, mufg_row_data)
        self.assertEqual(mufg_row.zaim_date, datetime(2018, 11, 5, 0, 0, 0))
        self.assertIsInstance(mufg_row.zaim_store, Store)
        self.assertIsNone(mufg_row.zaim_store.name_zaim)
        self.assertEqual(mufg_row.zaim_income_cash_flow_target, config_transfer_account_name)
        self.assertEqual(mufg_row.zaim_income_ammount_income, expected_amount)
        self.assertEqual(mufg_row.zaim_payment_cash_flow_source, config_account_name)
        self.assertEqual(mufg_row.zaim_payment_note, '')
        self.assertEqual(mufg_row.zaim_payment_amount_payment, expected_amount)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_source, config_account_name)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_target, config_transfer_account_name)
        self.assertEqual(mufg_row.zaim_transfer_amount_transfer, expected_amount)


class TestMufgTransferIncomeRow(ConfigurableDatabaseTestCase):
    """Tests for MufgTransferIncomeRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """Arguments should set into properties."""
        mufg_row_data = MufgRowData('2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金')
        expected_amount = 20
        transfer_target = '三菱UFJ銀行'
        store_name = '三菱UFJ銀行'
        mufg_row = MufgTransferIncomeRow(Account.MUFG, mufg_row_data)
        self.assertEqual(mufg_row.zaim_date, datetime(2018, 8, 20, 0, 0, 0))
        self.assertIsInstance(mufg_row.zaim_store, Store)
        self.assertEqual(mufg_row.zaim_store.name_zaim, store_name)
        self.assertEqual(mufg_row.zaim_income_cash_flow_target, transfer_target)
        self.assertEqual(mufg_row.zaim_income_ammount_income, expected_amount)
        self.assertEqual(mufg_row.zaim_payment_cash_flow_source, store_name)
        self.assertEqual(mufg_row.zaim_payment_note, '')
        self.assertEqual(mufg_row.zaim_payment_amount_payment, expected_amount)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_source, store_name)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_target, transfer_target)
        self.assertEqual(mufg_row.zaim_transfer_amount_transfer, expected_amount)


class TestMufgTransferPaymentRow(ConfigurableDatabaseTestCase):
    """Tests for MufgTransferPaymentRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """Arguments should set into properties."""
        mufg_row_data = MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '振替支払い')
        expected_amount = 3628
        config_account_name = '三菱UFJ銀行'
        transfer_target = 'ゴールドポイントカード・プラス'
        store_name = '東京都水道局　経理部管理課'
        mufg_row = MufgTransferPaymentRow(Account.MUFG, mufg_row_data)
        self.assertEqual(mufg_row.zaim_date, datetime(2018, 11, 28, 0, 0, 0))
        self.assertIsInstance(mufg_row.zaim_store, Store)
        self.assertEqual(mufg_row.zaim_store.name_zaim, store_name)
        self.assertEqual(mufg_row.zaim_income_cash_flow_target, transfer_target)
        self.assertEqual(mufg_row.zaim_income_ammount_income, expected_amount)
        self.assertEqual(mufg_row.zaim_payment_cash_flow_source, config_account_name)
        self.assertEqual(mufg_row.zaim_payment_note, '')
        self.assertEqual(mufg_row.zaim_payment_amount_payment, expected_amount)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_source, config_account_name)
        self.assertEqual(mufg_row.zaim_transfer_cash_flow_target, transfer_target)
        self.assertEqual(mufg_row.zaim_transfer_amount_transfer, expected_amount)


class TestMufgRowFactory(DatabaseTestCase):
    """Tests for MufgRowFactory."""

    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.expand([
        (MufgRowData('2018/10/1', 'カ－ド', '', '', '10000', '3000000', '', '',	'入金'),
         MufgIncomeRow),
        (MufgRowData('2018/11/5', 'カ－ド', '', '9000', '', '4000000', '', '', '支払い'),
         MufgPaymentRow),
        (MufgRowData('2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金'),
         MufgTransferIncomeRow),
        (MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '振替支払い'),
         MufgTransferPaymentRow),
    ])
    def test_create_success(self, argument, expected):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        mufg_row = MufgRowFactory().create(Account.MUFG, argument)
        self.assertIsInstance(mufg_row, expected)

    def test_create_fail(self):
        """Method should raise ValueError when note is not defined."""
        with self.assertRaises(ValueError):
            # pylint: disable=protected-access
            MufgRowFactory().create(
                Account.MUFG,
                MufgRowData('2018/11/28', '水道', 'トウキヨウトスイドウ', '3628', '', '5000000', '', '', '')
            )
