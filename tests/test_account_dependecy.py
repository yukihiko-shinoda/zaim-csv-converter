"""Tests for account_dependency.py ."""
from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.datasources.csv import CsvFactory
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.rowconverters.waon import WaonZaimRowConverterFactory


class TestAccount:
    """Tests for account dependency."""
    @staticmethod
    def test_convert_string_to_int_or_none():
        """
        Argument should set into properties.
        Default encode should be UTF-8.
        Default csv herder should be None.
        """
        file_name_csv_convert = FileCsvConvert.WAON
        regex_csv_file_name = r'.*waon.*\.csv'
        csv_factory = CsvFactory()
        input_row_data_class = WaonRowData
        input_row_factory = WaonRowFactory()
        zaim_row_factory_selector = WaonZaimRowConverterFactory()
        account_dependency = AccountContext(
            file_name_csv_convert, regex_csv_file_name, csv_factory,
            input_row_data_class, input_row_factory, zaim_row_factory_selector
        )
        assert account_dependency.file_csv_convert == file_name_csv_convert
        assert account_dependency.regex_csv_file_name == regex_csv_file_name
        assert account_dependency.csv_factory == csv_factory
        assert account_dependency.input_row_data_class == input_row_data_class
        assert account_dependency.input_row_factory == input_row_factory
        assert account_dependency.zaim_row_converter_selector == zaim_row_factory_selector
