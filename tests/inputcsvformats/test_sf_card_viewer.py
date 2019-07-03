#!/usr/bin/env python
"""Tests for sf_card_viewer.py."""
from datetime import datetime

import pytest
from parameterized import parameterized

from tests.resource import ConfigurableDatabaseTestCase, StoreFactory
from zaimcsvconverter import CONFIG
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowFactory, SFCardViewerRowData, \
    SFCardViewerExitByWindowRow, SFCardViewerAutoChargeRow, SFCardViewerSalesGoodsRow, SFCardViewerTransportationRow
from zaimcsvconverter.models import StoreRowData, Store
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimTransferRow


class TestSFCardViewerRowData:
    """Tests for SFCardViewerRowData."""

    def test_init_and_property(self):
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        used_date = '2018/11/13'
        is_commuter_pass_enter = ''
        railway_company_name_enter = 'メトロ'
        station_name_enter = '六本木一丁目'
        is_commuter_pass_exit = ''
        railway_company_name_exit = 'メトロ'
        station_name_exit = '後楽園'
        used_amount = '195'
        balance = '3601'
        note = ''
        sf_card_viewer_row_data = SFCardViewerRowData(used_date, is_commuter_pass_enter, railway_company_name_enter,
                                                      station_name_enter, is_commuter_pass_exit,
                                                      railway_company_name_exit, station_name_exit, used_amount,
                                                      balance, note)
        assert sf_card_viewer_row_data.is_commuter_pass_enter == is_commuter_pass_enter
        assert sf_card_viewer_row_data.railway_company_name_enter == railway_company_name_enter
        assert sf_card_viewer_row_data.station_name_enter == station_name_enter
        assert sf_card_viewer_row_data.is_commuter_pass_exit == is_commuter_pass_exit
        assert sf_card_viewer_row_data.railway_company_name_exit == railway_company_name_exit
        assert sf_card_viewer_row_data.used_amount == used_amount
        assert sf_card_viewer_row_data.balance == balance
        assert sf_card_viewer_row_data.note == note
        assert sf_card_viewer_row_data.date == datetime(2018, 11, 13, 0, 0)
        assert sf_card_viewer_row_data.store_name == station_name_exit


def prepare_fixture():
    """This function prepare common fixture with some tests."""
    StoreFactory(
        account=Account.PASMO,
        row_data=StoreRowData('後楽園', '東京地下鉄株式会社　南北線後楽園駅', '交通', '電車'),
    )
    StoreFactory(
        account=Account.PASMO,
        row_data=StoreRowData('北千住', '北千住', '交通', '電車'),
    )


class TestSFCardViewerRow(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_init(self):
        """
        Arguments should set into properties.
        """
        sf_card_viewer_row_data = SFCardViewerRowData(
            '2018/11/13', '', 'メトロ', '六本木一丁目', '', 'メトロ', '後楽園', '195', '3601', ''
        )
        expected_amount = 195
        config_account_name = 'PASMO'
        config_auto_charge_source = 'TOKYU CARD'
        sf_card_viewer_row = SFCardViewerTransportationRow(Account.PASMO, sf_card_viewer_row_data, CONFIG.pasmo)
        assert sf_card_viewer_row.zaim_date == datetime(2018, 11, 13, 0, 0, 0)
        assert isinstance(sf_card_viewer_row.zaim_store, Store)
        assert sf_card_viewer_row.zaim_store.name_zaim == '東京地下鉄株式会社　南北線後楽園駅'
        assert sf_card_viewer_row.zaim_payment_cash_flow_source == config_account_name
        assert sf_card_viewer_row.zaim_payment_note == 'メトロ 六本木一丁目 → メトロ 後楽園'
        assert sf_card_viewer_row.zaim_payment_amount_payment == expected_amount
        assert sf_card_viewer_row.zaim_transfer_cash_flow_source == config_auto_charge_source
        assert sf_card_viewer_row.zaim_transfer_cash_flow_target == config_account_name
        assert sf_card_viewer_row.zaim_transfer_amount_transfer == -1 * expected_amount


class TestSFCardViewerTransportationRow(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerTransportationRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_convert_to_zaim_row(self):
        """SFCardViewerTransportationRow should convert to ZaimPaymentRow."""
        sf_card_viewer_row = SFCardViewerTransportationRow(
            Account.PASMO,
            SFCardViewerRowData('2018/11/13', '', 'メトロ', '六本木一丁目', '', 'メトロ', '後楽園', '195', '3601', ''),
            CONFIG.pasmo
        )
        assert isinstance(sf_card_viewer_row.convert_to_zaim_row(), ZaimPaymentRow)


class TestSFCardViewerSalesGoodsRow(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerSalesGoodsRow."""
    sf_card_viewer_row = None

    def _prepare_fixture(self):
        prepare_fixture()
        self.sf_card_viewer_row = SFCardViewerSalesGoodsRow(
            Account.PASMO,
            SFCardViewerRowData('2018/11/14', '', '', '', '', '', '', '480', '3005', '物販'),
            CONFIG.pasmo
        )

    def test_convert_to_zaim_row(self):
        """SFCardViewerSalesGoodsRow should convert to ZaimPaymentRow."""
        assert isinstance(self.sf_card_viewer_row.convert_to_zaim_row(), ZaimPaymentRow)


class TestSFCardViewerSalesGoodsRowSkip(TestSFCardViewerSalesGoodsRow):
    """Tests for SFCardViewerSalesGoodsRow."""

    @property
    def source_yaml_file(self):
        return 'config_skip_sales_goods_row.yml.dist'

    def test_is_row_to_skip(self):
        """SFCardViewerSalesGoodsRow should convert to ZaimPaymentRow."""
        assert self.sf_card_viewer_row.is_row_to_skip


class TestSFCardViewerSalesGoodsRowNotSkip(TestSFCardViewerSalesGoodsRow):
    """Tests for SFCardViewerSalesGoodsRow."""

    @property
    def source_yaml_file(self):
        return 'config_not_skip_sales_goods_row.yml.dist'

    def test_is_row_to_skip(self):
        """SFCardViewerSalesGoodsRow should convert to ZaimPaymentRow."""
        assert not self.sf_card_viewer_row.is_row_to_skip


class TestSFCardViewerAutoChargeRow(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerTransportationRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_convert_to_zaim_row(self):
        """SFCardViewerTransportationRow should convert to ZaimTransferRow."""
        sf_card_viewer_row = SFCardViewerAutoChargeRow(
            Account.PASMO,
            SFCardViewerRowData('2018/11/11', '', 'JR東', '秋葉原', '', '', '', '-3000', '5022', 'ｵｰﾄﾁｬｰｼﾞ'),
            CONFIG.pasmo
        )
        assert isinstance(sf_card_viewer_row.convert_to_zaim_row(), ZaimTransferRow)


class TestSFCardViewerExitByWindowRow(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerTransportationRow."""

    def _prepare_fixture(self):
        prepare_fixture()

    def test_convert_to_zaim_row(self):
        """SFCardViewerTransportationRow should convert to ZaimPaymentRow."""
        sf_card_viewer_row = SFCardViewerExitByWindowRow(
            Account.PASMO,
            SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '0', '2621', '窓出'),
            CONFIG.pasmo
        )
        assert isinstance(sf_card_viewer_row.convert_to_zaim_row(), ZaimPaymentRow)

    @pytest.mark.parametrize('sf_card_viewer_row_data, expected', [
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', 'JR東', '北千住', '0', '2621', '窓出'),
         False),
        (SFCardViewerRowData('2018/11/25', '', '東武', 'とうきょうスカイツリー', '', '東武', '北千住', '0', '2621', '窓出'),
         False),
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '100', '2621', '窓出'),
         False),
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '0', '2621', '窓出'),
         True),
    ])
    def test_is_row_to_skip(self, sf_card_viewer_row_data, expected):
        """Method should return true when entered station is as same as exit station and used amount is 0."""
        sf_card_viewer_row = SFCardViewerExitByWindowRow(
            Account.PASMO,
            sf_card_viewer_row_data,
            CONFIG.pasmo
        )
        assert sf_card_viewer_row.is_row_to_skip == expected


class TestSFCardViewerRowFactory(ConfigurableDatabaseTestCase):
    """Tests for SFCardViewerRowFactory."""

    def _prepare_fixture(self):
        prepare_fixture()

    @pytest.mark.parametrize('argument, expected', [
        (SFCardViewerRowData('2018/11/13', '', 'メトロ', '六本木一丁目', '', 'メトロ', '後楽園', '195', '3601', ''),
         SFCardViewerTransportationRow),
        (SFCardViewerRowData('2018/11/14', '', '', '', '', '', '', '480', '3005', '物販'),
         SFCardViewerSalesGoodsRow),
        (SFCardViewerRowData('2018/11/11', '', 'JR東', '秋葉原', '', '', '', '-3000', '5022', 'ｵｰﾄﾁｬｰｼﾞ'),
         SFCardViewerAutoChargeRow),
        (SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '0', '2621', '窓出'),
         SFCardViewerExitByWindowRow),
    ])
    def test_create_success(self, argument, expected):
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        sf_card_viewer_row = SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(Account.PASMO, argument)
        assert isinstance(sf_card_viewer_row, expected)

    def test_create_fail(self):
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValueError):
            # pylint: disable=protected-access
            SFCardViewerRowFactory(lambda: CONFIG.pasmo).create(
                Account.PASMO,
                SFCardViewerRowData('2018/11/25', '', '東武', '北千住', '', '東武', '北千住', '0', '2621', 'ﾁｬｰｼﾞ')
            )
