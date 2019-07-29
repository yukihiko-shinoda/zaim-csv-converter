"""Tests for waon.py."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory, WaonRow, WaonChargeRow
from zaimcsvconverter.models import Store, AccountId


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
        assert waon_row_data.used_amount == 129
        assert waon_row_data.use_kind == WaonRowData.UseKind.PAYMENT
        assert waon_row_data.charge_kind == WaonRowData.ChargeKind.NULL

    @staticmethod
    # pylint: disable=unused-argument
    def test_validate(database_session_with_schema):
        """Validate method should collect errors."""
        assert InstanceResource.ROW_DATA_WAON_UNSUPPORTED_USE_KIND.validate
        assert str(
            # Reason: Pylint has not support dataclasses. pylint: disable=unsubscriptable-object
            InstanceResource.ROW_DATA_WAON_UNSUPPORTED_USE_KIND.list_error[0]
        ) == 'Invalid used amount. Use kind = 入金'


class TestWaonRow:
    """Tests for WaonRow."""
    # pylint: disable=too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize('waon_row_data, expected_date, expected_store_name_zaim, expected_amount', [
        (InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI, datetime(2018, 8, 7, 0, 0, 0),
         'ファミリーマート　かぶと町永代通り店', 129),
        (InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO, datetime(2018, 8, 30, 0, 0, 0),
         'イオンスタイル　板橋前野町', 1489),
    ])
    def test_init_success(yaml_config_load, database_session_basic_store_waon, waon_row_data, expected_date,
                          expected_store_name_zaim, expected_amount):
        """
        Arguments should set into properties.
        :param WaonRowData waon_row_data:
        """
        waon_row = WaonRow(AccountId.WAON, waon_row_data)
        assert waon_row.date == expected_date
        assert isinstance(waon_row.store, Store)
        assert waon_row.store.name_zaim == expected_store_name_zaim

    # pylint: disable=unused-argument
    @staticmethod
    def test_is_row_to_skip(database_session_basic_store_waon):
        """WaonRow which express download point should be row to skip."""
        assert WaonRow(
            AccountId.WAON, WaonRowData('2018/10/22', '板橋前野町', '0円', 'ポイントダウンロード', '-')
        ).is_row_to_skip


class TestWaonChargeRow:
    """Tests for WaonChargeRow."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema',
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=['database_session_with_schema']
    )
    def test_charge_kind_fail(yaml_config_load, database_session_with_schema):
        """Property should raise ValueError when charge kind is null on WAON charge row."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            WaonChargeRow(
                AccountId.WAON, InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO
            ).charge_kind
        assert str(error.value) == 'Charge kind on charge row is not allowed "-".'


class TestWaonRowFactory:
    """Tests for WaonRowFactory."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        'argument, expected_is_payment, expected_is_charge, expected_is_auto_charge, expected_is_download_point',
        [
            (InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI, True, False, False, False),
            (InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, False, True, False, False),
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, False, False, True, False),
            (InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO, False, False, False, True),
        ]
    )
    def test_create(database_session_basic_store_waon, argument, expected_is_payment, expected_is_charge,
                    expected_is_auto_charge, expected_is_download_point):
        """Method should return Store model when use kind is defined."""
        # pylint: disable=protected-access
        waon_row = WaonRowFactory().create(AccountId.WAON, argument)
        assert isinstance(waon_row, WaonRow)
        assert waon_row.is_payment == expected_is_payment
        assert waon_row.is_charge == expected_is_charge
        assert waon_row.is_auto_charge == expected_is_auto_charge
        assert waon_row.is_download_point == expected_is_download_point
