#!/usr/bin/env python
"""Tests for Config."""
from tests.resource import ConfigurableTestCase
from zaimcsvconverter import Config


class TestConfig(ConfigurableTestCase):
    """Tests for Config."""
    def test_init(self):
        """Constructor should leave to load yaml file."""
        config = Config()
        self.assertIsNone(config.waon)
        self.assertIsNone(config.gold_point_card_plus)
        self.assertIsNone(config.mufg)
        self.assertIsNone(config.pasmo)
        self.assertIsNone(config.amazon)

    def test_load(self):
        """Arguments should load yaml file."""
        config = Config()
        config.load()
        self.assertEqual(config.waon.account_name, 'WAON')
        self.assertEqual(config.waon.auto_charge_source, 'イオン銀行')
        self.assertEqual(config.gold_point_card_plus.account_name, 'ヨドバシゴールドポイントカード・プラス')
        self.assertEqual(config.gold_point_card_plus.skip_amazon_row, True)
        self.assertEqual(config.mufg.account_name, '三菱UFJ銀行')
        self.assertEqual(config.mufg.transfer_account_name, 'お財布')
        self.assertEqual(config.pasmo.account_name, 'PASMO')
        self.assertEqual(config.pasmo.auto_charge_source, 'TOKYU CARD')
        self.assertEqual(config.pasmo.skip_sales_goods_row, True)
        self.assertEqual(config.amazon.store_name_zaim, 'Amazon Japan G.K.')
        self.assertEqual(config.amazon.payment_account_name, 'ヨドバシゴールドポイントカード・プラス')
