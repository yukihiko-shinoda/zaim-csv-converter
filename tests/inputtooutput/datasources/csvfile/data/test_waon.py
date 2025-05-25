"""Tests for waon.py."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.data.waon import ChargeKind
from zaimcsvconverter.data.waon import UseKind
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.waon import WaonRowData


class TestWaonRowData:
    """Tests for WaonRowData."""

    @staticmethod
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        expected_amount = 129
        date = "2018/8/7"
        used_store = "ファミリーマートかぶと町永代"
        used_amount = "129円"
        use_kind = "支払"
        charge_kind = "-"
        waon_row_data = RowDataFactory(WaonRowData).create([date, used_store, used_amount, use_kind, charge_kind])
        assert_each_properties(
            waon_row_data,
            [
                # Reason: Time is not used in this process.
                datetime(2018, 8, 7, 0, 0),  # noqa: DTZ001
                used_store,
                expected_amount,
                UseKind.PAYMENT,
                ChargeKind.NULL,
            ],
        )

    @staticmethod
    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("database_session_with_schema")
    def test_validate() -> None:
        """Validate method should collect errors."""
        # - The key: `loc` of ValidationError should be not index but property name even if instantiate dataclass without kwarg? · Issue #9140 · pydantic/pydantic  # pylint: disable=line-too-long
        #   https://github.com/pydantic/pydantic/issues/9140
        index_use_kind = 3
        with pytest.raises(ValidationError) as excinfo:
            RowDataFactory(WaonRowData).create(InstanceResource.ROW_DATA_WAON_UNSUPPORTED_USE_KIND)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == (index_use_kind,)
        assert error["msg"] == (
            "Input should be "
            "'支払', '支払取消', 'チャージ', 'オートチャージ', "
            "'ポイントダウンロード', 'WAON移行（アップロード）' or 'WAON移行（ダウンロード）'"  # noqa: RUF001
        )

    @staticmethod
    def test_unsupported_charge_kind() -> None:
        """Unsupported charge kind should raise error."""
        # - The key: `loc` of ValidationError should be not index but property name even if instantiate dataclass without kwarg? · Issue #9140 · pydantic/pydantic  # pylint: disable=line-too-long
        #   https://github.com/pydantic/pydantic/issues/9140
        index_charge_kind = 4
        with pytest.raises(ValidationError) as excinfo:
            RowDataFactory(WaonRowData).create(InstanceResource.ROW_DATA_WAON_UNSUPPORTED_CHARGE_KIND)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == (index_charge_kind,)
        assert error["msg"] == "Input should be '銀行口座', 'ポイント', '現金', 'バリューダウンロード' or '-'"
