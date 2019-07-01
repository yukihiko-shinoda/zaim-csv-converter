#!/usr/bin/env python
"""Tests for zaim_row.py."""
from dataclasses import dataclass
from parameterized import parameterized

from tests.instance_fixture import InstanceFixture
from tests.resource import StoreFactory, ConfigurableDatabaseTestCase, ItemFactory
from zaimcsvconverter import CONFIG
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowFactory
from zaimcsvconverter.inputcsvformats.mufg import MufgTransferIncomeRow, MufgRowData
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData, SFCardViewerRowFactory
from zaimcsvconverter.inputcsvformats.waon import WaonAutoChargeRow, WaonRowData
from zaimcsvconverter.models import StoreRowData, ItemRowData
from zaimcsvconverter.zaim_row import ZaimIncomeRow, ZaimPaymentRow, ZaimTransferRow


@dataclass
class ZaimRowDataForTest:
    """This class implements data class for wrapping list of Zaim CSV row model."""
    date: str
    method: str
    category_large: str
    category_small: str
    cash_flow_source: str
    cash_flow_target: str
    item_name: str
    note: str
    store_name: str
    currency: str
    amount_income: str
    amount_payment: str
    amount_transfer: str
    balance_adjustment: str
    amount_before_currency_conversion: str
    setting_aggregate: str


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.MUFG,
        row_data=StoreRowData('スーパーフツウ', '三菱UFJ銀行', 'その他', 'その他', '臨時収入', ''),
    )
    StoreFactory(
        account=Account.PASMO,
        row_data=StoreRowData('後楽園', '東京地下鉄株式会社　南北線後楽園駅', '交通', '電車'),
    )
    ItemFactory(
        account=Account.AMAZON,
        row_data=ItemRowData('Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト', '大型出費', '家電'),
    )


class TestZaimIncomeRow(ConfigurableDatabaseTestCase):
    """Tests for ZaimIncomeRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    def test_all(self):
        """Argument should set into properties."""
        zaim_low = ZaimIncomeRow(MufgTransferIncomeRow(Account.MUFG, MufgRowData(
            '2018/8/20', '利息', 'スーパーフツウ', '', '20', '2000000', '', '', '振替入金'
        )))
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowDataForTest(*list_zaim_row)
        self.assertEqual(zaim_row_data.date, '2018-08-20')
        self.assertEqual(zaim_row_data.method, 'income')
        self.assertEqual(zaim_row_data.category_large, '臨時収入')
        self.assertEqual(zaim_row_data.category_small, '-')
        self.assertEqual(zaim_row_data.cash_flow_source, '')
        self.assertEqual(zaim_row_data.cash_flow_target, '三菱UFJ銀行')
        self.assertEqual(zaim_row_data.item_name, '')
        self.assertEqual(zaim_row_data.note, '')
        self.assertEqual(zaim_row_data.store_name, '三菱UFJ銀行')
        self.assertEqual(zaim_row_data.currency, '')
        self.assertEqual(zaim_row_data.amount_income, 20)
        self.assertEqual(zaim_row_data.amount_payment, 0)
        self.assertEqual(zaim_row_data.amount_transfer, 0)
        self.assertEqual(zaim_row_data.balance_adjustment, '')
        self.assertEqual(zaim_row_data.amount_before_currency_conversion, '')
        self.assertEqual(zaim_row_data.setting_aggregate, '')


class TestZaimPaymentRow(ConfigurableDatabaseTestCase):
    """Tests for ZaimPaymentRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    # pylint: disable=too-many-arguments,too-many-locals
    @parameterized.expand([
        (SFCardViewerRowFactory(lambda: CONFIG.pasmo), Account.PASMO, SFCardViewerRowData(
            '2018/11/13', '', 'メトロ', '六本木一丁目', '', 'メトロ', '後楽園', '195', '3601', ''
        ), '2018-11-13', '交通', '電車', 'PASMO', None, 'メトロ 六本木一丁目 → メトロ 後楽園',
         '東京地下鉄株式会社　南北線後楽園駅', 195),
        (AmazonRowFactory(), Account.AMAZON, InstanceFixture.ROW_DATA_AMAZON,
         '2018-10-23', '大型出費', '家電', 'ヨドバシゴールドポイントカード・プラス',
         'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト', '',
         'Amazon Japan G.K.', 4980),
    ])
    def test_all(self, input_row_factory, account, input_row_data, expected_date, expected_category_large,
                 expected_category_small, expected_cash_flow_source, expected_item_name, expected_note,
                 expected_store_name, expected_amount_payment):
        """Argument should set into properties."""
        zaim_low = ZaimPaymentRow(input_row_factory.create(account, input_row_data))
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowDataForTest(*list_zaim_row)
        self.assertEqual(zaim_row_data.date, expected_date)
        self.assertEqual(zaim_row_data.method, 'payment')
        self.assertEqual(zaim_row_data.category_large, expected_category_large)
        self.assertEqual(zaim_row_data.category_small, expected_category_small)
        self.assertEqual(zaim_row_data.cash_flow_source, expected_cash_flow_source)
        self.assertEqual(zaim_row_data.cash_flow_target, '')
        self.assertEqual(zaim_row_data.item_name, expected_item_name)
        self.assertEqual(zaim_row_data.note, expected_note)
        self.assertEqual(zaim_row_data.store_name, expected_store_name)
        self.assertEqual(zaim_row_data.currency, '')
        self.assertEqual(zaim_row_data.amount_income, 0)
        self.assertEqual(zaim_row_data.amount_payment, expected_amount_payment)
        self.assertEqual(zaim_row_data.amount_transfer, 0)
        self.assertEqual(zaim_row_data.balance_adjustment, '')
        self.assertEqual(zaim_row_data.amount_before_currency_conversion, '')
        self.assertEqual(zaim_row_data.setting_aggregate, '')


class TestZaimTransferRow(ConfigurableDatabaseTestCase):
    """Tests for ZaimTransferRow."""
    def _prepare_fixture(self):
        prepare_fixture()

    def test_all(self):
        """Argument should set into properties."""
        zaim_low = ZaimTransferRow(WaonAutoChargeRow(Account.WAON, WaonRowData(
            '2018/11/11', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座')))
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowDataForTest(*list_zaim_row)
        self.assertEqual(zaim_row_data.date, '2018-11-11')
        self.assertEqual(zaim_row_data.method, 'transfer')
        self.assertEqual(zaim_row_data.category_large, '-')
        self.assertEqual(zaim_row_data.category_small, '-')
        self.assertEqual(zaim_row_data.cash_flow_source, 'イオン銀行')
        self.assertEqual(zaim_row_data.cash_flow_target, 'WAON')
        self.assertEqual(zaim_row_data.item_name, '')
        self.assertEqual(zaim_row_data.note, '')
        self.assertEqual(zaim_row_data.store_name, '')
        self.assertEqual(zaim_row_data.currency, '')
        self.assertEqual(zaim_row_data.amount_income, 0)
        self.assertEqual(zaim_row_data.amount_payment, 0)
        self.assertEqual(zaim_row_data.amount_transfer, 5000)
        self.assertEqual(zaim_row_data.balance_adjustment, '')
        self.assertEqual(zaim_row_data.amount_before_currency_conversion, '')
        self.assertEqual(zaim_row_data.setting_aggregate, '')
