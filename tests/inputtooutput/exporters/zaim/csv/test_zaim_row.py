"""Tests for zaim_row.py."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import cast

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
from zaimcsvconverter.inputtooutput.datasources.csv.records.waon import WaonChargeRow, WaonStoreRow
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import (
    ZaimIncomeRow,
    ZaimPaymentRow,
    ZaimRow,
    ZaimTransferRow,
)


@pytest.fixture(scope="class")
def zaim_row_data_created_by_zaim_row(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_item_class_scope: None,  # noqa: ARG001
    account: Account,
    input_row_data: InputRowData,
) -> ZaimRowData:
    csv_record_processor = CsvRecordProcessor(account.value.input_row_factory)
    input_row = csv_record_processor.create_input_row_instance(input_row_data)
    # Reason: Pylint's bug. pylint: disable=no-member
    zaim_low = ZaimRowFactory.create(account.value.zaim_row_converter_factory.create(input_row, Path()))
    list_zaim_row = zaim_low.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@pytest.mark.parametrize(
    ["account", "input_row_data"],
    [(Account.MUFG, InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT)],
    scope="class",
)
class TestZaimIncomeRow:
    """Tests for ZaimIncomeRow."""

    def test_date(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.date == "2018-08-20"

    def test_method(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.method == "income"

    def test_category_large(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.category_large == "臨時収入"

    def test_category_small(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.category_small == "-"

    def test_cash_flow_source(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.cash_flow_source

    def test_cash_flow_target(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.cash_flow_target == "三菱UFJ銀行"

    def test_item_name(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.item_name

    def test_note(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.note

    def test_store_name(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.store_name == "三菱UFJ銀行"

    def test_currency(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.currency

    def test_amount_income(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        expected_amount_income = 20
        assert zaim_row_data_created_by_zaim_row.amount_income == expected_amount_income

    def test_amount_payment(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.amount_payment == 0

    def test_amount_transfer(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert zaim_row_data_created_by_zaim_row.amount_transfer == 0

    def test_balance_adjustment(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.balance_adjustment

    def test_amount_before_currency_conversion(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.amount_before_currency_conversion

    def test_setting_aggregate(self, zaim_row_data_created_by_zaim_row: ZaimRowData) -> None:
        """Argument should set into properties."""
        assert not zaim_row_data_created_by_zaim_row.setting_aggregate


@pytest.fixture(scope="class")
def zaim_row_data_created_by_zaim_payment_row(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_item_class_scope: None,  # noqa: ARG001
    input_row_factory: InputRowFactory[InputRowData, InputRow[InputRowData]],
    input_row_data: InputRowData,
    zaim_row_converter_factory: CsvRecordToZaimRowConverterFactory[InputRow[InputRowData], InputRowData],
) -> ZaimRowData:
    input_row = input_row_factory.create(input_row_data)
    zaim_low = ZaimRowFactory.create(zaim_row_converter_factory.create(input_row, Path()))
    list_zaim_row = zaim_low.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@dataclass
class Expected:
    date: str
    category_large: str
    category_small: str
    cash_flow_source: str
    item_name: str
    note: str
    store_name: str
    amount_payment: int
    method: str = "payment"
    cash_flow_target: str = ""
    amount_income: int = 0
    amount_transfer: int = 0
    currency: str = ""
    balance_adjustment: str = ""
    amount_before_currency_conversion: str = ""
    setting_aggregate: str = ""


@pytest.mark.parametrize(
    ("input_row_factory", "input_row_data", "zaim_row_converter_factory", "expected"),
    [
        (
            SFCardViewerRowFactory(lambda: CONFIG.pasmo),
            InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
            SFCardViewerZaimRowConverterFactory(lambda: CONFIG.pasmo),
            Expected(
                "2018-11-13",
                "交通",
                "電車",
                "PASMO",
                "",
                "メトロ 六本木一丁目 → メトロ 後楽園",
                "東京地下鉄株式会社　南北線後楽園駅",
                195,
            ),
        ),
        (
            AmazonRowFactory(),
            InstanceResource.ROW_DATA_AMAZON_ECHO_DOT,
            AmazonZaimRowConverterFactory(),
            Expected(
                "2018-10-23",
                "大型出費",
                "家電",
                "ヨドバシゴールドポイントカード・プラス",
                "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
                "",
                "Amazon Japan G.K.",
                4980,
            ),
        ),
    ],
    scope="class",
)
class TestZaimPaymentRow:
    """Tests for ZaimPaymentRow."""

    def test_date(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.date == expected.date

    def test_method(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.method == expected.method

    def test_category_large(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.category_large == expected.category_large

    def test_category_small(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.category_small == expected.category_small

    def test_cash_flow_source(
        self,
        zaim_row_data_created_by_zaim_payment_row: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.cash_flow_source == expected.cash_flow_source

    def test_cash_flow_target(
        self,
        zaim_row_data_created_by_zaim_payment_row: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.cash_flow_target == expected.cash_flow_target

    def test_item_name(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.item_name == expected.item_name

    def test_note(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.note == expected.note

    def test_store_name(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.store_name == expected.store_name

    def test_currency(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.currency == expected.currency

    def test_amount_income(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.amount_income == expected.amount_income

    def test_amount_payment(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.amount_payment == expected.amount_payment

    def test_amount_transfer(self, zaim_row_data_created_by_zaim_payment_row: ZaimRowData, expected: Expected) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.amount_transfer == expected.amount_transfer

    def test_balance_adjustment(
        self,
        zaim_row_data_created_by_zaim_payment_row: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.balance_adjustment == expected.balance_adjustment

    def test_amount_before_currency_conversion(
        self,
        zaim_row_data_created_by_zaim_payment_row: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.amount_before_currency_conversion == expected.amount_before_currency_conversion

    def test_setting_aggregate(
        self,
        zaim_row_data_created_by_zaim_payment_row: ZaimRowData,
        expected: Expected,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_payment_row
        assert zaim_row_data.setting_aggregate == expected.setting_aggregate


@dataclass
class ExpectedTransfer:
    date: str = "2018-11-11"
    method: str = "transfer"
    category_large: str = "-"
    category_small: str = "-"
    cash_flow_source: str = "イオン銀行"
    cash_flow_target: str = "WAON"
    item_name: str = ""
    note: str = ""
    store_name: str = ""
    amount_transfer: int = 5000
    amount_income: int = 0
    amount_payment: int = 0
    currency: str = ""
    balance_adjustment: str = ""
    amount_before_currency_conversion: str = ""
    setting_aggregate: str = ""


@pytest.mark.parametrize(
    ["account", "input_row_data", "expected"],
    [(Account.WAON, InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO, ExpectedTransfer())],
    scope="class",
)
class TestZaimTransferRow:
    """Tests for ZaimTransferRow."""

    def test_date(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.date == expected.date

    def test_method(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.method == expected.method

    def test_category_large(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.category_large == expected.category_large

    def test_category_small(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.category_small == expected.category_small

    def test_cash_flow_source(
        self,
        zaim_row_data_created_by_zaim_row: ZaimRowData,
        expected: ExpectedTransfer,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.cash_flow_source == expected.cash_flow_source

    def test_cash_flow_target(
        self,
        zaim_row_data_created_by_zaim_row: ZaimRowData,
        expected: ExpectedTransfer,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.cash_flow_target == expected.cash_flow_target

    def test_item_name(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.item_name == expected.item_name

    def test_note(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.note == expected.note

    def test_store_name(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.store_name == expected.store_name

    def test_currency(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.currency == expected.currency

    def test_amount_income(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.amount_income == expected.amount_income

    def test_amount_payment(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.amount_payment == expected.amount_payment

    def test_amount_transfer(self, zaim_row_data_created_by_zaim_row: ZaimRowData, expected: ExpectedTransfer) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.amount_transfer == expected.amount_transfer

    def test_balance_adjustment(
        self,
        zaim_row_data_created_by_zaim_row: ZaimRowData,
        expected: ExpectedTransfer,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.balance_adjustment == expected.balance_adjustment

    def test_before_currency_conversion(
        self,
        zaim_row_data_created_by_zaim_row: ZaimRowData,
        expected: ExpectedTransfer,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.amount_before_currency_conversion == expected.amount_before_currency_conversion

    def test_setting_aggregate(
        self,
        zaim_row_data_created_by_zaim_row: ZaimRowData,
        expected: ExpectedTransfer,
    ) -> None:
        """Argument should set into properties."""
        zaim_row_data = zaim_row_data_created_by_zaim_row
        assert zaim_row_data.setting_aggregate == expected.setting_aggregate


class TestZaimRowFactory:
    """Tests for ZaimRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        ("database_session_with_schema", "zaim_row_converter_class", "input_row_class", "waon_row_data", "expected"),
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
                WaonStoreRow,
                InstanceResource.ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO,
                ZaimPaymentRow,
            ),
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                WaonZaimTransferRowConverter,
                WaonStoreRow,
                InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO,
                ZaimTransferRow,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_success(
        zaim_row_converter_class: type[ZaimRowConverter[WaonStoreRow, WaonRowData]],
        input_row_class: type[WaonStoreRow],
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
                return datetime.now(tz=timezone(timedelta(hours=+9), "JST"))

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
        with pytest.raises(
            ValueError,
            match=r"Undefined\sZaim\srow\sconverter\.\sZaim\srow\sconverter\s\=\sUndefinedZaimRowConverter",
        ):
            ZaimRowFactory.create(UndefinedZaimRowConverter(undefined_input_row))
