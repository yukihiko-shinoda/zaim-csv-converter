"""Tests for gold_point_card_plus.py."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.account import Account
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus import (
    GoldPointCardPlusZaimPaymentRowConverter,
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.zaim_row import ZaimPaymentRow


class TestGoldPointCardPlusZaimPaymentRowConverter:
    """Tests for GoldPointCardPlusZaimPaymentRowConverter."""

    # Reason: Testing different version of row data is better to be separated code.
    # noinspection DuplicatedCode
    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        "gold_point_card_plus_row_data, expected_date, expected_store_name_zaim, expected_use_amount",
        [
            (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC, "2018-07-03", "東京電力エナジーパートナー株式会社", 11402),
            (InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP, "2018-07-04", "Amazon Japan G.K.", 3456),
        ],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_gold_point_card_plus")
    def test(
        gold_point_card_plus_row_data: GoldPointCardPlusRowData,
        expected_date: str,
        expected_store_name_zaim: str,
        expected_use_amount: int,
    ) -> None:
        """Arguments should set into properties."""
        account_context = Account.GOLD_POINT_CARD_PLUS.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        row = csv_record_processor.create_input_row_instance(gold_point_card_plus_row_data)
        # Reason: Pylint's bug. pylint: disable=no-member
        zaim_row = ZaimRowFactory.create(account_context.zaim_row_converter_factory.create(row))
        assert isinstance(zaim_row, ZaimPaymentRow)
        list_zaim_row = zaim_row.convert_to_list()
        zaim_row_data = ZaimRowData(*list_zaim_row)
        assert zaim_row_data.date == expected_date
        assert zaim_row_data.store_name == expected_store_name_zaim
        assert zaim_row_data.item_name == ""
        assert zaim_row_data.cash_flow_source == "ヨドバシゴールドポイントカード・プラス"
        assert zaim_row_data.amount_payment == expected_use_amount


class TestGoldPointCardPlusZaimRowConverterFactory:
    """Tests for GoldPointCardPlusZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, input_row_data, expected",
        [
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP],
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                GoldPointCardPlusZaimPaymentRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test_select_factory(
        input_row_data: GoldPointCardPlusRowData, expected: type[GoldPointCardPlusZaimPaymentRowConverter]
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        account_context = Account.GOLD_POINT_CARD_PLUS.value
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        input_row = csv_record_processor.create_input_row_instance(input_row_data)
        actual = account_context.zaim_row_converter_factory.create(input_row)
        assert isinstance(actual, expected)
