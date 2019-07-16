"""Tests for waon.py."""
from datetime import datetime

import pytest

from tests.instance_fixture import InstanceFixture
from zaimcsvconverter.inputcsvformats.waon import WaonPaymentRow, WaonAutoChargeRow, WaonRowData, WaonRowFactory, \
    WaonChargeRow, WaonDownloadPointRow
from zaimcsvconverter.account import Account
from zaimcsvconverter.models import Store
from zaimcsvconverter.zaim_row import ZaimPaymentRow, ZaimIncomeRow, ZaimTransferRow


class TestWaonRowData:
    """Tests for WaonRowData."""
    @staticmethod
    def test_init_and_property():
        """
        Property date should return datetime object.
        Property store_date should return used_store.
        """
        date = '2018/8/7'
        used_store = 'ファミリーマートかぶと町永代'
        used_amount = '129円'
        use_kind = '支払'
        charge_kind = '-'
        waon_row_data = WaonRowData(date, used_store, used_amount, use_kind, charge_kind)
        assert waon_row_data.date == datetime(2018, 8, 7, 0, 0)
        assert waon_row_data.store_name == used_store
        assert waon_row_data.used_amount == used_amount
        assert waon_row_data.use_kind == use_kind
        assert waon_row_data.charge_kind == charge_kind


class TestWaonRow:
    """Tests for WaonRow."""
    # pylint: disable=too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        (
            'waon_row_data, expected_date, expected_store_name_zaim, '
            'expected_amount, expected_charge_kind'
        ),
        [
            (InstanceFixture.ROW_DATA_WAON, datetime(2018, 8, 7, 0, 0, 0),
             'ファミリーマート　かぶと町永代通り店', 129, None),
            (WaonRowData('2018/8/30', '板橋前野町', '1,489円', '支払', '-'), datetime(2018, 8, 30, 0, 0, 0),
             'イオンスタイル　板橋前野町', 1489, None),
        ]
    )
    def test_init_success(waon_row_data, expected_date, expected_store_name_zaim,
                          expected_amount, expected_charge_kind, yaml_config_load, database_session_basic_store_waon):
        """
        Arguments should set into properties.
        :param WaonRowData waon_row_data:
        """
        config_account_name = 'WAON'
        config_auto_charge_source = 'イオン銀行'
        waon_row = WaonPaymentRow(Account.WAON, waon_row_data)
        assert waon_row.zaim_date == expected_date
        assert isinstance(waon_row.zaim_store, Store)
        assert waon_row.zaim_store.name_zaim == expected_store_name_zaim
        assert waon_row.zaim_income_cash_flow_target == config_account_name
        assert waon_row.zaim_income_ammount_income == expected_amount
        assert waon_row.zaim_payment_cash_flow_source == config_account_name
        assert waon_row.zaim_payment_amount_payment == expected_amount
        assert waon_row.zaim_transfer_cash_flow_source == config_auto_charge_source
        assert waon_row.zaim_transfer_cash_flow_target == config_account_name
        assert waon_row.zaim_transfer_amount_transfer == expected_amount
        # pylint: disable=protected-access
        assert waon_row._charge_kind == expected_charge_kind

    # pylint: disable=unused-argument
    @staticmethod
    def test_init_fail(yaml_config_load, database_session_basic_store_waon):
        """Constructor should raise ValueError when got undefined charge kind."""
        with pytest.raises(ValueError):
            WaonPaymentRow(Account.WAON, WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '129円', '支払', 'クレジットカード'))


class TestWaonPaymentRow:
    """Tests for WaonPaymentRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_zaim_row_class_to_convert(yaml_config_load, database_session_basic_store_waon):
        """WaonPaymentRow should convert to ZaimPaymentRow."""
        waon_row = WaonPaymentRow(Account.WAON, InstanceFixture.ROW_DATA_WAON)
        validated_input_row = waon_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == ZaimPaymentRow


class TestWaonChargeRow:
    """Tests for WaonChargeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('waon_row_data, zaim_row_class', [
        (WaonRowData('2018/10/22', '板橋前野町', '1,504円', 'チャージ', 'ポイント'), ZaimIncomeRow),
        (WaonRowData('2018/11/11', '板橋前野町', '5,000円', 'チャージ', '銀行口座'), ZaimTransferRow),
    ])
    def test_zaim_row_class_to_convert(
            waon_row_data, zaim_row_class, yaml_config_load, database_session_basic_store_waon
    ):
        """
        WaonChargeRow for point should convert to ZaimIncomeRow.
        WaonChargeRow for bank account should convert to ZaimTransferRow.
        """
        waon_row = WaonChargeRow(Account.WAON, waon_row_data)
        validated_input_row = waon_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == zaim_row_class


class TestWaonAutoChargeRow:
    """Tests for WaonAutoChargeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_zaim_row_class_to_convert(yaml_config_load, database_session_basic_store_waon):
        """WaonAutoChargeRow should convert to ZaimTransferRow."""
        waon_row = WaonAutoChargeRow(Account.WAON,
                                     WaonRowData('2018/11/11', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'))
        validated_input_row = waon_row.validate()
        assert validated_input_row.zaim_row_class_to_convert() == ZaimTransferRow


@pytest.fixture
def waon_row():
    """This fixture prepares WaonDownloadPointRow instance."""
    yield WaonDownloadPointRow(Account.WAON, WaonRowData('2018/10/22', '板橋前野町', '0円', 'ポイントダウンロード', '-'))


class TestWaonDownloadPointRow:
    """Tests for WaonDownloadPointRow."""
    # pylint: disable=unused-argument
    @staticmethod
    def test_zaim_row_class_to_convert(database_session_basic_store_waon, waon_row):
        """WaonDownloadPointRow should raise ValueError when convert to ZaimRow."""
        with pytest.raises(ValueError):
            validated_input_row = waon_row.validate()
            validated_input_row.zaim_row_class_to_convert()

    # pylint: disable=unused-argument
    @staticmethod
    def test_is_row_to_skip(database_session_basic_store_waon, waon_row):
        """WaonDownloadPointRow should be row to skip."""
        assert waon_row.is_row_to_skip


class TestWaonRowFactory:
    """Tests for WaonRowFactory."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize('argument, expected', [
        (InstanceFixture.ROW_DATA_WAON, WaonPaymentRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'チャージ', 'ポイント'), WaonChargeRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'オートチャージ', '銀行口座'), WaonAutoChargeRow),
        (WaonRowData('2018/8/22', '板橋前野町', '5,000円', 'ポイントダウンロード', '-'), WaonDownloadPointRow),
    ])
    def test_create_success(argument, expected, database_session_basic_store_waon):
        """Method should return Store model when use kind is defined."""
        # pylint: disable=protected-access
        waon_row = WaonRowFactory().create(Account.WAON, argument)
        assert isinstance(waon_row, expected)

    # pylint: disable=unused-argument
    @staticmethod
    def test_create_fail(database_session_basic_store_waon):
        """Method should raise ValueError when use kind is not defined."""
        with pytest.raises(ValueError):
            # pylint: disable=protected-access
            WaonRowFactory().create(Account.WAON, WaonRowData('2018/8/7', 'ファミリーマートかぶと町永代', '10000円', '入金', '-'))
