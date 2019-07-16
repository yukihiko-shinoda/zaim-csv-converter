"""This module implements converting steps from account CSV to Zaim CSV."""
from zaimcsvconverter import CONFIG
from zaimcsvconverter.input_csv_converter_iterator import InputCsvConverterIterator
from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.models import initialize_database


class ZaimCsvConverter:
    """This class implements converting steps from account CSV to Zaim CSV."""
    @staticmethod
    def execute() -> None:
        """This method executes all CSV converters."""
        CONFIG.load()
        initialize_database()
        ConvertTableImporter().execute()
        InputCsvConverterIterator().execute()
