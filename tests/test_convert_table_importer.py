"""Tests for convert_table_importer.py."""

from pathlib import Path
from typing import Any

import pytest
from sqlalchemy.orm.session import Session as SQLAlchemySession

from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.models import Item, Store


class TestConvertTableImporter:
    """Tests for ConvertTableImporter."""

    def _prepare_fixture(self) -> None:
        pass

    def test_success(self, database_session_with_schema: SQLAlchemySession, resource_path: Path) -> None:
        """CSV should import into appropriate table."""
        for path in sorted(resource_path.glob("*.csv")):
            ConvertTableImporter.execute(path)
        self.assert_store_equal(
            [
                [1, 3, "", None, None, None, None, "お財布"],
                [2, 3, "トウキヨウガス", "東京ガス（株）", "水道・光熱", "ガス料金", None, None],  # noqa: RUF001
                [3, 3, "ＧＰマーケテイング", None, None, None, None, "ゴールドポイントカード・プラス"],
                [4, 3, "トウキヨウトスイドウ", "東京都水道局　経理部管理課", "水道・光熱", "水道料金", None, None],
                [
                    5,
                    1,
                    "ファミリーマートかぶと町永代",
                    "ファミリーマート　かぶと町永代通り店",
                    "食費",
                    "食料品",
                    None,
                    None,
                ],
                [6, 1, "板橋前野町", "イオンスタイル　板橋前野町", "食費", "食料品", "その他", None],
            ],
            database_session_with_schema,
        )
        self.assert_item_equal(
            [
                [1, 5, "（Amazon ポイント）", "通信", "その他"],  # noqa: RUF001
                [2, 5, "（Amazonポイント）", "通信", "その他"],  # noqa: RUF001
                [3, 5, "（割引）", "通信", "その他"],  # noqa: RUF001
                [4, 5, "（配送料・手数料）", "通信", "宅配便"],  # noqa: RUF001
                [
                    5,
                    5,
                    "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
                    "大型出費",
                    "家電",
                ],
                [
                    6,
                    5,
                    "".join(
                        [
                            "LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 ",  # noqa: RUF001
                            "机の擦り傷防止滑り止め カート可能 透明大型デスク足元マット ",
                            "フローリング/畳/床暖房対応 (120×90cm)",  # noqa: RUF001
                        ],
                    ),
                    "住まい",
                    "家具",
                ],
            ],
            database_session_with_schema,
        )

    def assert_store_equal(
        self,
        expected_stores: list[list[Any]],
        database_session_with_schema: SQLAlchemySession,
    ) -> None:
        """This method asserts Store table."""
        # Reeason: SQLAlchemy 2 Stubs' issue:
        # - any, has on column attribute · Issue #207 · sqlalchemy/sqlalchemy2-stubs
        #   https://github.com/sqlalchemy/sqlalchemy2-stubs/issues/207
        stores: list[Store] = database_session_with_schema.query(Store).order_by(Store.id.asc()).all()
        assert len(stores) == len(expected_stores)
        for store, expected_store in zip(stores, expected_stores):
            self.assert_store1(store, expected_store)
            self.assert_store2(store, expected_store)

    @staticmethod
    def assert_store1(store: Store, expected_store: list[Any]) -> None:
        assert store.id == expected_store[0]
        assert store.file_csv_convert_id == expected_store[1]
        assert store.name == expected_store[2]
        assert store.name_zaim == expected_store[3]

    @staticmethod
    def assert_store2(store: Store, expected_store: list[Any]) -> None:
        assert store.category_payment_large == expected_store[4]
        assert store.category_payment_small == expected_store[5]
        assert store.category_income == expected_store[6]
        assert store.transfer_target == expected_store[7]

    def assert_item_equal(
        self,
        expected_items: list[list[Any]],
        database_session_with_schema: SQLAlchemySession,
    ) -> None:
        """This method asserts Store table."""
        # Reeason: SQLAlchemy 2 Stubs' issue:
        # - any, has on column attribute · Issue #207 · sqlalchemy/sqlalchemy2-stubs
        #   https://github.com/sqlalchemy/sqlalchemy2-stubs/issues/207
        items: list[Item] = database_session_with_schema.query(Item).order_by(Item.id.asc()).all()
        assert len(items) == len(expected_items)
        for item, expected_item in zip(items, expected_items):
            self.assert_item1(item, expected_item)
            self.assert_item2(item, expected_item)

    @staticmethod
    def assert_item1(item: Item, expected_item: list[Any]) -> None:
        assert item.id == expected_item[0]
        assert item.file_csv_convert_id == expected_item[1]
        assert item.name == expected_item[2]

    @staticmethod
    def assert_item2(item: Item, expected_item: list[Any]) -> None:
        assert item.category_payment_large == expected_item[3]
        assert item.category_payment_small == expected_item[4]

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_with_schema")
    def test_fail(resource_path: Path) -> None:
        """Method should raise error when the file which name is not correct is included."""
        for path in sorted(resource_path.glob("[!I]*.csv")):
            ConvertTableImporter.execute(path)
        with pytest.raises(
            ValueError,
            match=r"can\'t\sdetect\saccount\stype\sby\scsv\sfile\sname\.\sPlease\sconfirm\scsv\sfile\sname\.",
        ):
            ConvertTableImporter.execute(resource_path / "invalid.csv")
