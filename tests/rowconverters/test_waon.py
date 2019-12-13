"""Tests for waon.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory, WaonRow
from zaimcsvconverter.models import AccountId
from zaimcsvconverter.zaim_row import ZaimTransferRow, ZaimPaymentRow, ZaimIncomeRow, ZaimRowFactory
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterFactory, WaonZaimPaymentRowConverter, \
    WaonZaimIncomeRowConverter, WaonZaimTransferRowConverter


class TestWaonZaimIncomeRowConverter:
    """Tests for WaonZaimIncomeRowConverter."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        'waon_row_data, expected_date, expected_store, expected_amount_income',
        [
            (InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, '2018-10-22', 'イオンスタイル　板橋前野町', 1504),
        ]
    )
    def test(waon_row_data, expected_date, expected_store, expected_amount_income,
             yaml_config_load, database_session_basic_store_waon):
        """Arguments should set into properties."""
        waon_row = WaonRow(AccountId.WAON, waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(WaonZaimIncomeRowConverter(waon_row))
        assert isinstance(zaim_row, ZaimIncomeRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_target == 'WAON'
        assert zaim_row_data.amount_income == expected_amount_income


class TestWaonZaimPaymentRowConverter:
    """Tests for WaonZaimPaymentRowConverter."""
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        'waon_row_data, expected_date, expected_store, expected_amount_payment',
        [
            (InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
             '2018-08-07', 'ファミリーマート　かぶと町永代通り店', 129),
            (InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
             '2018-08-30', 'イオンスタイル　板橋前野町', 1489),
        ]
    )
    def test(waon_row_data, expected_date, expected_store, expected_amount_payment,
             yaml_config_load, database_session_basic_store_waon):
        """Arguments should set into properties."""
        waon_row = WaonRow(AccountId.WAON, waon_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(WaonZaimPaymentRowConverter(waon_row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store
        assert zaim_row_data.item_name == ''
        assert zaim_row_data.cash_flow_source == 'WAON'
        assert zaim_row_data.amount_payment == expected_amount_payment


class TestWaonZaimTransferRowConverter:
    """Tests for WaonZaimTransferRowConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'waon_row_data, expected_date, expected_amount_payment',
        [
            # 1. auto charge
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, '2018-11-11', 5000),
            # 2. charge from bank account
            (InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO, '2018-10-22', 10000),
        ]
    )
    def test(waon_row_data, expected_date, expected_amount_payment,
             yaml_config_load, database_session_basic_store_waon):
        """Arguments should set into properties."""
        waon_row = WaonRow(AccountId.WAON, waon_row_data)
        zaim_row = ZaimRowFactory.create(WaonZaimTransferRowConverter(waon_row))
        assert isinstance(zaim_row, ZaimTransferRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.cash_flow_source == 'イオン銀行'
        assert zaim_row_data.cash_flow_target == 'WAON'
        assert zaim_row_data.amount_transfer == expected_amount_payment


class TestWaonZaimRowConverterConverter:
    """Tests for WaonZaimRowConverterConverter."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, input_row_data, expected',
        [
            # Case when WAON payment
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI],
             InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI, WaonZaimPaymentRowConverter),
            # Case when WAON charge from point
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
             InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, WaonZaimIncomeRowConverter),
            # Case when WAON auto charge
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
             InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, WaonZaimTransferRowConverter),
            # Case when WAON charge by bank account
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
             InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO, WaonZaimTransferRowConverter),
            # Case when WAON charge by cash
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
             InstanceResource.ROW_DATA_WAON_CHARGE_CASH_ITABASHIMAENOCHO, WaonZaimTransferRowConverter),
        ], indirect=['database_session_with_schema']
    )
    def test_success(yaml_config_load, database_session_with_schema, input_row_data: WaonRowData, expected):
        """Input row should convert to suitable ZaimRow by transfer target."""
        input_row = WaonRowFactory().create(AccountId.WAON, input_row_data)
        assert isinstance(WaonZaimRowConverterFactory().create(input_row), expected)

    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema',
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=['database_session_with_schema']
    )
    def test_fail(yaml_config_load, database_session_with_schema):
        """Create method should raise ValueError when input row is undefined type."""
        input_row = WaonRowFactory().create(AccountId.WAON,
                                            InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO)
        with pytest.raises(ValueError) as error:
            WaonZaimRowConverterFactory().create(input_row)
        assert str(error.value) == 'Unsupported row. Input row = WaonRow, UseKind.DOWNLOAD_POINT'
