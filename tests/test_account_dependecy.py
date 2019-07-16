"""Tests for account_dependency.py ."""
from zaimcsvconverter.account_dependency import AccountDependency
from zaimcsvconverter.inputcsvformats.waon import WaonRowData, WaonRowFactory
from zaimcsvconverter.models import Store


class TestAccount:
    """Tests for account dependency."""
    @staticmethod
    def test_convert_string_to_int_or_none():
        """
        Argument should set into properties.
        Default encode should be UTF-8.
        Default csv herder should be None.
        """
        identity = 1
        file_name_csv_convert = 'waon.csv'
        regex_csv_file_name = r'.*waon.*\.csv'
        convert_table_model_class = Store
        input_row_data_class = WaonRowData
        input_row_factory = WaonRowFactory()
        account_dependency = AccountDependency(identity, file_name_csv_convert, regex_csv_file_name,
                                               convert_table_model_class, input_row_data_class, input_row_factory)
        assert account_dependency.id == identity
        assert account_dependency.file_name_csv_convert == file_name_csv_convert
        assert account_dependency.regex_csv_file_name == regex_csv_file_name
        assert account_dependency.convert_table_model_class == convert_table_model_class
        assert account_dependency.input_row_data_class == input_row_data_class
        assert account_dependency.input_row_factory == input_row_factory
        assert account_dependency.encode == 'UTF-8'
        assert account_dependency.csv_header is None
