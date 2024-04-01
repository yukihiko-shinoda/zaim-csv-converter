"""Tests for WaonRowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.waon import WaonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonRowToSkip, WaonStoreRow


class TestWaonRowFactory:
    """Tests for WaonRowFactory."""

    @staticmethod
    @pytest.mark.usefixtures("database_session_basic_store_waon")
    def test_create_waon_row_to_skip() -> None:
        """Method should return Store model when use kind is defined."""
        # pylint: disable=protected-access
        row_data = InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO
        waon_row = WaonRowFactory().create(row_data)
        assert isinstance(waon_row, WaonRowToSkip)

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("row_data", "property_name_true"),
        [
            (InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI, "is_payment"),
            (InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, "is_charge"),
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, "is_auto_charge"),
        ],
    )
    @pytest.mark.usefixtures("database_session_basic_store_waon")
    def test_create_waon_row(row_data: WaonRowData, property_name_true: str) -> None:
        """Method should return Store model when use kind is defined."""
        list_property_use_kind = [
            "is_payment",
            "is_payment_cancel",
            "is_charge",
            "is_auto_charge",
        ]
        # pylint: disable=protected-access
        waon_row = WaonRowFactory().create(row_data)
        assert isinstance(waon_row, WaonStoreRow)
        for property_use_kind in list_property_use_kind:
            assert getattr(waon_row, property_use_kind) == (property_use_kind == property_name_true)
