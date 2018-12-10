#!/usr/bin/env python
"""Tests for AmazonRow."""
from datetime import datetime

import unittest2 as unittest
from parameterized import parameterized

from tests.instance_fixture import InstanceFixture
from tests.resource import ItemFactory, ConfigurableDatabaseTestCase
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData, AmazonRow, AmazonRowFactory
from zaimcsvconverter.models import ItemRowData, Store, Item
from zaimcsvconverter.zaim_row import ZaimPaymentRow


class TestAmazonRowData(unittest.TestCase):
    """Tests for AmazonRowData."""
    # pylint: disable=too-many-locals
    def test_init_and_property(self):
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        ordered_date = '2018/10/23'
        order_id = '123-4567890-1234567'
        item_name = 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト'
        note = '販売： Amazon Japan G.K.  コンディション： 新品'
        price = '4980'
        number = '1'
        subtotal_price_item = '6276'
        total_order = '6390'
        destination = 'ローソン桜塚'
        status = '2018年10月23日に発送済み'
        billing_address = 'テストアカウント'
        billing_amount = '5952'
        credit_card_billing_date = '2018/10/23'
        credit_card_billing_amount = '5952'
        credit_card_identity = 'Visa（下4けたが1234）'
        url_order_summary = 'https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=123-4567890-1234567'
        url_receipt = \
            'https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi?ie=UTF8&orderID=123-4567890-1234567'
        url_item = 'https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1'
        row_data = AmazonRowData(ordered_date, order_id, item_name, note, price, number, subtotal_price_item,
                                 total_order, destination, status, billing_address, billing_amount,
                                 credit_card_billing_date, credit_card_billing_amount, credit_card_identity,
                                 url_order_summary, url_receipt, url_item)
        self.assertEqual(row_data.order_id, order_id)
        self.assertEqual(row_data.note, note)
        self.assertEqual(row_data.price, price)
        self.assertEqual(row_data.number, number)
        self.assertEqual(row_data.subtotal_price_item, subtotal_price_item)
        self.assertEqual(row_data.total_order, total_order)
        self.assertEqual(row_data.destination, destination)
        self.assertEqual(row_data.status, status)
        self.assertEqual(row_data.billing_address, billing_address)
        self.assertEqual(row_data.billing_amount, billing_amount)
        self.assertEqual(row_data.credit_card_billing_date, credit_card_billing_date)
        self.assertEqual(row_data.credit_card_billing_amount, credit_card_billing_amount)
        self.assertEqual(row_data.credit_card_identity, credit_card_identity)
        self.assertEqual(row_data.url_order_summary, url_order_summary)
        self.assertEqual(row_data.url_receipt, url_receipt)
        self.assertEqual(row_data.url_item, url_item)
        self.assertEqual(row_data.date, datetime(2018, 10, 23, 0, 0))
        self.assertEqual(row_data.item_name, item_name)


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    ItemFactory(
        account=Account.AMAZON,
        row_data=ItemRowData('Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト', '大型出費', '家電'),
    )


class TestAmazonRow(ConfigurableDatabaseTestCase):
    """Tests for MufgTransferIncomeRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """Arguments should set into properties."""
        expected_amount = 4980
        store_name = 'Amazon Japan G.K.'
        item_name = 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト'
        mufg_row = AmazonRow(Account.AMAZON, InstanceFixture.ROW_DATA_AMAZON)
        self.assertEqual(mufg_row.price, 4980)
        self.assertEqual(mufg_row.number, 1)
        self.assertEqual(mufg_row.zaim_date, datetime(2018, 10, 23, 0, 0, 0))
        self.assertIsInstance(mufg_row.zaim_store, Store)
        self.assertEqual(mufg_row.zaim_store.name_zaim, store_name)
        self.assertIsInstance(mufg_row.zaim_item, Item)
        self.assertEqual(mufg_row.zaim_item.name, item_name)
        self.assertEqual(mufg_row.zaim_payment_cash_flow_source, 'ヨドバシゴールドポイントカード・プラス')
        self.assertEqual(mufg_row.zaim_payment_note, '')
        self.assertEqual(mufg_row.zaim_payment_amount_payment, expected_amount)

    def test_convert_to_zaim_row(self):
        """MufgTransferIncomeRow should convert to suitable ZaimRow by transfer target."""
        mufg_row = AmazonRow(Account.AMAZON, InstanceFixture.ROW_DATA_AMAZON)
        self.assertIsInstance(mufg_row.convert_to_zaim_row(), ZaimPaymentRow)


class TestAmazonRowFactory(ConfigurableDatabaseTestCase):
    """Tests for AmazonRowFactory."""

    def _prepare_fixture(self):
        prepare_fixture()

    @parameterized.expand([
        (InstanceFixture.ROW_DATA_AMAZON, AmazonRow),
    ])
    def test_create(self, argument, expected):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = AmazonRowFactory().create(Account.AMAZON, argument)
        self.assertIsInstance(gold_point_card_plus_row, expected)
