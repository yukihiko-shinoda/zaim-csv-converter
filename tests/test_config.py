"""Tests for Config."""
from pathlib import Path

from tests.testlibraries.assert_list import assert_each_properties
from zaimcsvconverter.config import Config


class TestConfig:
    """Tests for Config."""

    # pylint: disable=unused-argument
    def test_init(self) -> None:
        """Constructor should leave to load yaml file."""
        config = Config()
        assert_each_properties(config, [None, None, None, None, None, None, None, None, None, None])

    def test_load(self, resource_path_root: Path) -> None:
        """Arguments should load yaml file."""
        config = Config()
        config.load(resource_path_root / "config.yml.dist")
        self.assert_waon(config, "WAON", "イオン銀行")
        self.assert_gold_point_card_plus(
            config,
            "ヨドバシゴールドポイントカード・プラス",
            skip_amazon_row=True,
            skip_pay_pal_row=True,
            skip_kyash_row=True,
        )
        self.assert_mufg(config, "三菱UFJ銀行", "お財布", "三菱UFJ銀行")
        self.assert_pasmo(config, "PASMO", "TOKYU CARD", skip_sales_goods_row=True)
        assert config.amazon.store_name_zaim == "Amazon Japan G.K."
        assert config.amazon.payment_account_name == "ヨドバシゴールドポイントカード・プラス"

    @staticmethod
    def assert_waon(config: Config, account_name: str, auto_charge_source: str) -> None:
        assert config.waon.account_name == account_name
        assert config.waon.auto_charge_source == auto_charge_source

    @staticmethod
    def assert_gold_point_card_plus(
        config: Config,
        account_name: str,
        *,
        skip_amazon_row: bool,
        skip_pay_pal_row: bool,
        skip_kyash_row: bool,
    ) -> None:
        """Arguments should set into properties."""
        assert config.gold_point_card_plus.account_name == account_name
        assert config.gold_point_card_plus.skip_amazon_row == skip_amazon_row
        assert config.gold_point_card_plus.skip_pay_pal_row == skip_pay_pal_row
        assert config.gold_point_card_plus.skip_kyash_row == skip_kyash_row

    @staticmethod
    def assert_mufg(config: Config, account_name: str, transfer_account_name: str, store_name_zaim: str) -> None:
        assert config.mufg.account_name == account_name
        assert config.mufg.transfer_account_name == transfer_account_name
        assert config.mufg.store_name_zaim == store_name_zaim

    @staticmethod
    def assert_pasmo(
        config: Config,
        account_name: str,
        auto_charge_source: str,
        *,
        skip_sales_goods_row: bool,
    ) -> None:
        """Arguments should set into properties."""
        assert config.pasmo.account_name == account_name
        assert config.pasmo.auto_charge_source == auto_charge_source
        assert config.pasmo.skip_sales_goods_row == skip_sales_goods_row
