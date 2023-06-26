"""Tests for WaonRowFactory."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.waon import WaonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonRow


class TestWaonRowFactory:
    """Tests for WaonRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("argument", "property_name_true"),
        [
            (InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI, "is_payment"),
            (InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO, "is_charge"),
            (InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, "is_auto_charge"),
            (InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO, "is_download_point"),
        ],
    )
    @pytest.mark.usefixtures("database_session_basic_store_waon")
    def test_create(argument: WaonRowData, property_name_true: str) -> None:
        """Method should return Store model when use kind is defined."""
        list_property_use_kind = [
            "is_payment",
            "is_payment_cancel",
            "is_charge",
            "is_auto_charge",
            "is_download_point",
            "is_transfer_waon_upload",
            "is_transfer_waon_download",
        ]
        # pylint: disable=protected-access
        waon_row = WaonRowFactory().create(argument)
        assert isinstance(waon_row, WaonRow)
        for property_use_kind in list_property_use_kind:
            assert getattr(waon_row, property_use_kind) == (property_use_kind == property_name_true)
