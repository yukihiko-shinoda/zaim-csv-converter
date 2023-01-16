"""Tests for zaim_row.py."""
from datetime import datetime
from pathlib import Path
from typing import cast, Type

import pytest
from returns.primitives.hkt import Kind1

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputtooutput.converters.recordtozaim import (
    CsvRecordToZaimRowConverterFactory,
    ZaimRowConverter,
    ZaimRowFactory,
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon import AmazonZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sf_card_viewer import SFCardViewerZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import (
    WaonZaimIncomeRowConverter,
    WaonZaimPaymentRowConverter,
    WaonZaimTransferRowConverter,
)
from zaimcsvconverter.inputtooutput.datasources.csv.converters.amazon import AmazonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.converters.sf_card_viewer import SFCardViewerRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.datasources.csv.data import InputRowData
from zaimcsvconverter.inputtooutput.datasources.csv.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputRow
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonChargeRow, WaonRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import (
    ZaimIncomeRow,
    ZaimPaymentRow,
    ZaimRow,
    ZaimTransferRow,
)


class TestZaimIncomeRow:
    """Tests for ZaimIncomeRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_item")
    def test_all() -> None:
        """Argument should set into properties."""
        account_context = Account.MUFG.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        mufg_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT
        )
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_low = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(mufg_row, Path()))
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-08-20"
        assert zaim_row_data.method == "income"
        assert zaim_row_data.category_large == "臨時収入"
        assert zaim_row_data.category_small == "-"
        assert zaim_row_data.cash_flow_source == ""
        assert zaim_row_data.cash_flow_target == "三菱UFJ銀行"
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.note == ""
        assert zaim_row_data.store_name == "三菱UFJ銀行"
        assert zaim_row_data.currency == ""
        assert zaim_row_data.amount_income == 20
        assert zaim_row_data.amount_payment == 0
        assert zaim_row_data.amount_transfer == 0
        assert zaim_row_data.balance_adjustment == ""
        assert zaim_row_data.amount_before_currency_conversion == ""
        assert zaim_row_data.setting_aggregate == ""


class TestZaimPaymentRow:
    """Tests for ZaimPaymentRow."""

    # pylint: disable=too-many-arguments,too-many-locals,unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        (
            "input_row_factory, input_row_data, zaim_row_converter_factory, expected_date, "
            "expected_category_large, expected_category_small, expected_cash_flow_source, expected_item_name, "
            "expected_note, expected_store_name, expected_amount_payment"
        ),
        [
            (
                SFCardViewerRowFactory(lambda: CONFIG.pasmo),
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
                SFCardViewerZaimRowConverterFactory(lambda: CONFIG.pasmo),
                "2018-11-13",
                "交通",
                "電車",
                "PASMO",
                "",
                "メトロ 六本木一丁目 → メトロ 後楽園",
                "東京地下鉄株式会社　南北線後楽園駅",
                195,
            ),
            (
                AmazonRowFactory(),
                InstanceResource.ROW_DATA_AMAZON_ECHO_DOT,
                AmazonZaimRowConverterFactory(),
                "2018-10-23",
                "大型出費",
                "家電",
                "ヨドバシゴールドポイントカード・プラス",
                "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
                "",
                "Amazon Japan G.K.",
                4980,
            ),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_item")
    def test_all(
        input_row_factory: InputRowFactory[InputRowData, InputRow[InputRowData]],
        input_row_data: InputRowData,
        zaim_row_converter_factory: CsvRecordToZaimRowConverterFactory[InputRow[InputRowData], InputRowData],
        expected_date: str,
        expected_category_large: str,
        expected_category_small: str,
        expected_cash_flow_source: str,
        expected_item_name: str,
        expected_note: str,
        expected_store_name: str,
        expected_amount_payment: int,
    ) -> None:
        """Argument should set into properties."""
        input_row = input_row_factory.create(input_row_data)
        zaim_low = ZaimRowFactory.create(zaim_row_converter_factory.create(input_row, Path()))
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.method == "payment"
        assert zaim_row_data.category_large == expected_category_large
        assert zaim_row_data.category_small == expected_category_small
        assert zaim_row_data.cash_flow_source == expected_cash_flow_source
        assert zaim_row_data.cash_flow_target == ""
        assert zaim_row_data.item_name == expected_item_name
        assert zaim_row_data.note == expected_note
        assert zaim_row_data.store_name == expected_store_name
        assert zaim_row_data.currency == ""
        assert zaim_row_data.amount_income == 0
        assert zaim_row_data.amount_payment == expected_amount_payment
        assert zaim_row_data.amount_transfer == 0
        assert zaim_row_data.balance_adjustment == ""
        assert zaim_row_data.amount_before_currency_conversion == ""
        assert zaim_row_data.setting_aggregate == ""


class TestZaimTransferRow:
    """Tests for ZaimTransferRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_item")
    def test_all() -> None:
        """Argument should set into properties."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        waon_auto_charge_row = csv_record_processor.create_input_row_instance(
            InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO
        )
        zaim_low = ZaimRowFactory.create(
            account_context.zaim_row_converter_factory.create(waon_auto_charge_row, Path())
        )
        list_zaim_row = zaim_low.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == "2018-11-11"
        assert zaim_row_data.method == "transfer"
        assert zaim_row_data.category_large == "-"
        assert zaim_row_data.category_small == "-"
        assert zaim_row_data.cash_flow_source == "イオン銀行"
        assert zaim_row_data.cash_flow_target == "WAON"
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.note == ""
        assert zaim_row_data.store_name == ""
        assert zaim_row_data.currency == ""
        assert zaim_row_data.amount_income == 0
        assert zaim_row_data.amount_payment == 0
        assert zaim_row_data.amount_transfer == 5000
        assert zaim_row_data.balance_adjustment == ""
        assert zaim_row_data.amount_before_currency_conversion == ""
        assert zaim_row_data.setting_aggregate == ""


class TestZaimRowFactory:
    """Tests for ZaimRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, zaim_row_converter_class, input_row_class, waon_row_data, expected",
        [
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                WaonZaimIncomeRowConverter,
                WaonChargeRow,
                InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO,
                ZaimIncomeRow,
            ),
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                WaonZaimPaymentRowConverter,
                WaonRow,
                InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
                ZaimPaymentRow,
            ),
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                WaonZaimTransferRowConverter,
                WaonRow,
                InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO,
                ZaimTransferRow,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_success(
        zaim_row_converter_class: type[ZaimRowConverter[WaonRow, WaonRowData]],
        input_row_class: Type[WaonRow],
        waon_row_data: WaonRowData,
        expected: type[ZaimRow],
    ) -> None:
        """Factory should create appropriate type of Zaim row."""
        account_context = Account.WAON.value
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        input_row = csv_record_processor.create_input_row_instance(waon_row_data)
        assert isinstance(input_row, input_row_class)
        zaim_row_converter = account_context.zaim_row_converter_factory.create(input_row, Path())
        assert isinstance(zaim_row_converter, zaim_row_converter_class)
        assert isinstance(ZaimRowFactory.create(zaim_row_converter), expected)

    @staticmethod
    def test_fail() -> None:
        """Factory should raise ValueError when input row is undefined type."""

        # Reason: This class is just for test. pylint: disable=too-few-public-methods
        class UndefinedZaimRowConverter(ZaimRowConverter[InputRow[InputRowData], InputRowData]):
            pass

        class UndefinedInputRow(InputRow[InputRowData]):
            pass

        class UndefinedInputRowData(InputRowData):
            # Reason: Raw code is simple enough. pylint: disable=missing-docstring
            @property
            def date(self) -> datetime:
                return datetime.now()

            @property
            def store_name(self) -> str:
                return ""

            @property
            def item_name(self) -> str:
                return ""

            @property
            def validate(self) -> bool:
                return False

        undefined_input_row = cast(
            Kind1[InputRow[InputRowData], InputRowData],
            UndefinedInputRow(UndefinedInputRowData()),
        )
        with pytest.raises(ValueError) as error:
            ZaimRowFactory.create(UndefinedZaimRowConverter(undefined_input_row))
        assert str(error.value) == "Undefined Zaim row converter. Zaim row converter = UndefinedZaimRowConverter"
