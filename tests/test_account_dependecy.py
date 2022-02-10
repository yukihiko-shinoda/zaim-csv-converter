"""Tests for account_dependency.py ."""
from godslayer.god_slayer_factory import GodSlayerFactory

from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterFactory


class TestAccount:
    """Tests for account dependency."""

    @staticmethod
    def test_convert_string_to_int_or_none():
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        regex_csv_file_name = r".*waon.*\.csv"
        god_slayer_factory = GodSlayerFactory()
        input_row_data_class = WaonRowData
        input_row_factory = WaonRowFactory()
        zaim_row_factory_selector = WaonZaimRowConverterFactory()
        account_context = AccountContext(
            regex_csv_file_name,
            god_slayer_factory,
            input_row_data_class,
            input_row_factory,
            zaim_row_factory_selector,
        )
        assert account_context.regex_csv_file_name == regex_csv_file_name
        assert account_context.god_slayer_factory == god_slayer_factory
        assert account_context.input_row_data_class == input_row_data_class
        assert account_context.input_row_factory == input_row_factory
        assert account_context.zaim_row_converter_selector == zaim_row_factory_selector
