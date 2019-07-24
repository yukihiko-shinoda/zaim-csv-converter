"""Tests for Config."""
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter import Config


class TestConfig:
    """Tests for Config."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_init():
        """Constructor should leave to load yaml file."""
        config = Config()
        assert config.waon is None
        assert config.gold_point_card_plus is None
        assert config.mufg is None
        assert config.pasmo is None
        assert config.amazon is None

    # pylint: disable=unused-argument
    @staticmethod
    def test_load():
        """Arguments should load yaml file."""
        config = Config()
        config.load(InstanceResource.PATH_FILE_CONFIG_FOR_TEST)
        assert config.waon.account_name == 'WAON'
        assert config.waon.auto_charge_source == 'イオン銀行'
        assert config.gold_point_card_plus.account_name == 'ヨドバシゴールドポイントカード・プラス'
        assert config.gold_point_card_plus.skip_amazon_row
        assert config.mufg.account_name == '三菱UFJ銀行'
        assert config.mufg.transfer_account_name == 'お財布'
        assert config.pasmo.account_name == 'PASMO'
        assert config.pasmo.auto_charge_source == 'TOKYU CARD'
        assert config.pasmo.skip_sales_goods_row
        assert config.amazon.store_name_zaim == 'Amazon Japan G.K.'
        assert config.amazon.payment_account_name == 'ヨドバシゴールドポイントカード・プラス'
