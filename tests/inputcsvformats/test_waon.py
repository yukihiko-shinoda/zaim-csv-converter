"""Tests for waon.py."""
from datetime import datetime

from pydantic import ValidationError
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputcsvformats import RowDataFactory
from zaimcsvconverter.inputcsvformats.waon import (
    ChargeKind,
    UseKind,
    WaonChargeRow,
    WaonRow,
    WaonRowData,
    WaonRowFactory,
)
from zaimcsvconverter.models import Store


class TestWaonRowData:
    """Tests for WaonRowData."""

    @staticmethod
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        date = "2018/8/7"
        used_store = "ファミリーマートかぶと町永代"
        used_amount = "129円"
        use_kind = "支払"
        charge_kind = "-"
        waon_row_data = RowDataFactory(WaonRowData).create([date, used_store, used_amount, use_kind, charge_kind])
        assert waon_row_data.date == datetime(2018, 8, 7, 0, 0)
        assert waon_row_data.store_name == used_store
        assert waon_row_data.used_amount == 129
        assert waon_row_data.use_kind == UseKind.PAYMENT
        assert waon_row_data.charge_kind == ChargeKind.NULL

    @staticmethod
    # pylint: disable=unused-argument
    @pytest.mark.usefixtures("database_session_with_schema")
    def test_validate() -> None:
        """Validate method should collect errors."""
        with pytest.raises(ValidationError) as excinfo:
            RowDataFactory(WaonRowData).create(InstanceResource.ROW_DATA_WAON_UNSUPPORTED_USE_KIND)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == ("use_kind",)
        assert error["msg"] == (
            "value is not a valid enumeration member; permitted: "
            "'支払', '支払取消', 'チャージ', 'オートチャージ', "
            "'ポイントダウンロード', 'WAON移行（アップロード）', 'WAON移行（ダウンロード）'"
        )

    @staticmethod
    def test_unsupported_charge_kind() -> None:
        """Unsupported charge kind should raise error."""
        with pytest.raises(ValidationError) as excinfo:
            RowDataFactory(WaonRowData).create(InstanceResource.ROW_DATA_WAON_UNSUPPORTED_CHARGE_KIND)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == ("charge_kind",)
        assert error["msg"] == (
            "value is not a valid enumeration member; permitted: " "'銀行口座', 'ポイント', '現金', 'バリューダウンロード', '-'"
        )


class TestWaonRow:
    """Tests for WaonRow."""

    # pylint: disable=too-many-arguments,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "waon_row_data, expected_date, expected_store_name_zaim, expected_amount",
        [
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                datetime(2018, 8, 7, 0, 0, 0),
                "ファミリーマート　かぶと町永代通り店",
                129,
            ),
            (
                InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
                datetime(2018, 8, 30, 0, 0, 0),
                "イオンスタイル　板橋前野町",
                1489,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_basic_store_waon")
    def test_init_success(
        waon_row_data: WaonRowData,
        expected_date: datetime,
        expected_store_name_zaim: str,
        expected_amount: int,
    ) -> None:
        """Arguments should set into properties.

        :param WaonRowData waon_row_data:
        """
        waon_row = WaonRow(waon_row_data)
        assert waon_row.date == expected_date
        assert isinstance(waon_row.store, Store)
        assert waon_row.store.name_zaim == expected_store_name_zaim
        assert waon_row.used_amount == expected_amount

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_basic_store_waon")
    def test_is_row_to_skip() -> None:
        """WaonRow which express download point should be row to skip."""
        waon_row_data_factory = RowDataFactory(WaonRowData)
        assert WaonRow(waon_row_data_factory.create(["2018/10/22", "板橋前野町", "0円", "ポイントダウンロード", "-"])).is_row_to_skip
        assert WaonRow(
            waon_row_data_factory.create(["2020/10/23", "イオン銀行ＭＳ板橋区役所前１", "9,863円", "WAON移行（アップロード）", "-"])
        ).is_row_to_skip
        assert WaonRow(
            waon_row_data_factory.create(["2020/10/23", "イオン銀行ＭＳ板橋区役所前１", "9,863円", "WAON移行（ダウンロード）", "-"])
        ).is_row_to_skip


class TestWaonChargeRow:
    """Tests for WaonChargeRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema",
        [[InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO]],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_charge_kind_fail() -> None:
        """Property should raise ValueError when charge kind is null on WAON charge row."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            WaonChargeRow(InstanceResource.ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO).charge_kind
        assert str(error.value) == 'Charge kind on charge row is not allowed "-".'


class TestWaonRowFactory:
    """Tests for WaonRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "argument, property_name_true",
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
