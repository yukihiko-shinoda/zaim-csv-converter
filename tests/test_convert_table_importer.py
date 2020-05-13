"""Tests for convert_table_importer.py."""
from pathlib import Path
from typing import List

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.models import Store, Item


@pytest.fixture
def fixture_convert_table_importer(request, resource_path_root):
    """This fixture prepares ConvertTableImporter instance."""
    return ConvertTableImporter(resource_path_root / Path(__file__).stem / request.node.name)


class TestConvertTableImporter:
    """Tests for ConvertTableImporter"""
    def _prepare_fixture(self):
        pass

    def test_success(self, database_session_with_schema, fixture_convert_table_importer):
        """CSV should import into appropriate table."""
        fixture_convert_table_importer.execute()
        self.assert_store_equal([
            [1, 3, '', None, None, None, None, 'お財布'],
            [2, 3, 'トウキヨウガス', '東京ガス（株）', '水道・光熱', 'ガス料金', None, None],
            [3, 3, 'ＧＰマーケテイング', None, None, None, None, 'ゴールドポイントカード・プラス'],
            [4, 3, 'トウキヨウトスイドウ', '東京都水道局　経理部管理課', '水道・光熱', '水道料金', None, None],
            [5, 1, 'ファミリーマートかぶと町永代', 'ファミリーマート　かぶと町永代通り店', '食費', '食料品', None, None],
            [6, 1, '板橋前野町', 'イオンスタイル　板橋前野町', '食費', '食料品', 'その他', None],
        ], database_session_with_schema)
        self.assert_item_equal([
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
        ], database_session_with_schema)

    @staticmethod
    def assert_store_equal(expected_stores, database_session_with_schema):
        """This method asserts Store table."""
        stores: List[Store] = database_session_with_schema.query(Store).order_by(Store.id.asc()).all()
        assert len(stores) == len(expected_stores)
        index = 0
        for store in stores:
            expected_store = expected_stores[index]
            assert store.id == expected_store[0]
            assert store.file_csv_convert_id == expected_store[1]
            assert store.name == expected_store[2]
            assert store.name_zaim == expected_store[3]
            assert store.category_payment_large == expected_store[4]
            assert store.category_payment_small == expected_store[5]
            assert store.category_income == expected_store[6]
            assert store.transfer_target == expected_store[7]
            index += 1

    @staticmethod
    def assert_item_equal(expected_items, database_session_with_schema):
        """This method asserts Store table."""
        items: List[Item] = database_session_with_schema.query(Item).order_by(Item.id.asc()).all()
        assert len(items) == len(expected_items)
        index = 0
        for item in items:
            expected_item = expected_items[index]
            assert item.id == expected_item[0]
            assert item.file_csv_convert_id == expected_item[1]
            assert item.name == expected_item[2]
            assert item.category_payment_large == expected_item[3]
            assert item.category_payment_small == expected_item[4]
            index += 1

    # pylint: disable=unused-argument
    @staticmethod
    def test_fail(fixture_convert_table_importer, database_session_with_schema):
        """Method should raise error when the file which name is not correct is included."""
        with pytest.raises(ValueError):
            fixture_convert_table_importer.execute()
