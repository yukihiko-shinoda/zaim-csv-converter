#!/usr/bin/env python
"""Tests for convert_table_importer.py."""
from typing import List

from tests.resource import DatabaseTestCase, create_path_as_same_as_file_name
from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.models import Store, Item


class TestConvertTableImporter(DatabaseTestCase):
    """Tests for ConvertTableImporter"""
    convert_table_importer = None

    def _prepare_fixture(self):
        pass

    def setUp(self):
        super().setUp()
        self.convert_table_importer = ConvertTableImporter(
            create_path_as_same_as_file_name(self) / self._testMethodName
        )

    def test_success(self):
        """CSV should import into appropriate table."""
        self.convert_table_importer.execute()
        self.assertStoreEqual([
            [1, 3, '', None, None, None, None, 'お財布'],
            [2, 3, 'トウキヨウガス', '東京ガス（株）', '水道・光熱', 'ガス料金', None, None],
            [3, 3, 'ＧＰマーケテイング', None, None, None, None, 'ゴールドポイントカード・プラス'],
            [4, 3, 'トウキヨウトスイドウ', '東京都水道局　経理部管理課', '水道・光熱', '水道料金', None, None],
            [5, 1, 'ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店', '食費', '食料品', None, None],
            [6, 1, '板橋前野町', 'イオンスタイル　板橋前野町', '食費', '食料品', 'その他', None],
        ])
        self.assertItemEqual([
            [1, 5, '（Amazon ポイント）', '通信', 'その他'],
            [2, 5, '（Amazonポイント）', '通信', 'その他'],
            [3, 5, '（割引）', '通信', 'その他'],
            [4, 5, '（配送料・手数料）', '通信', '宅配便'],
            [5, 5, 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト', '大型出費', '家電'],
            [
                6,
                5,
                'LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 机の擦り傷防止滑り止め カート可能 透明大型デスク足元マット フローリング/畳/床暖房対応 (120×90cm)',
                '住まい',
                '家具'
            ],
        ])

    # pylint: disable=invalid-name
    def assertStoreEqual(self, expected_stores):
        """This method asserts Store table."""
        stores: List[Store] = self._session.query(Store).order_by(Store.id.asc()).all()
        self.assertEqual(len(stores), len(expected_stores))
        index = 0
        for store in stores:
            expected_store = expected_stores[index]
            self.assertEqual(store.id, expected_store[0])
            self.assertEqual(store.account_id, expected_store[1])
            self.assertEqual(store.name, expected_store[2])
            self.assertEqual(store.name_zaim, expected_store[3])
            self.assertEqual(store.category_payment_large, expected_store[4])
            self.assertEqual(store.category_payment_small, expected_store[5])
            self.assertEqual(store.category_income, expected_store[6])
            self.assertEqual(store.transfer_target, expected_store[7])
            index += 1

    # pylint: disable=invalid-name
    def assertItemEqual(self, expected_items):
        """This method asserts Store table."""
        items: List[Item] = self._session.query(Item).order_by(Item.id.asc()).all()
        self.assertEqual(len(items), len(expected_items))
        index = 0
        for item in items:
            expected_item = expected_items[index]
            self.assertEqual(item.id, expected_item[0])
            self.assertEqual(item.account_id, expected_item[1])
            self.assertEqual(item.name, expected_item[2])
            self.assertEqual(item.category_payment_large, expected_item[3])
            self.assertEqual(item.category_payment_small, expected_item[4])
            index += 1

    def test_fail(self):
        """Method should raise error when the file which name is not correct is included."""
        with self.assertRaises(ValueError):
            self.convert_table_importer.execute()
