"""This module implements converting steps from account CSV to Zaim CSV."""

from zaimcsvconverter import CONFIG, DirectoryCsv, PATH_FILE_CONFIG
from zaimcsvconverter.convert_table_importer import ConvertTableImporter
from zaimcsvconverter.errorreporters.error_totalizer import ErrorTotalizer
from zaimcsvconverter.exceptions import SomeInvalidInputCsvError
from zaimcsvconverter.models import initialize_database


class ZaimCsvConverter:
    """This class implements converting steps from account CSV to Zaim CSV."""

    @staticmethod
    def execute() -> None:
        """This method executes all CSV converters."""
        CONFIG.load(PATH_FILE_CONFIG)
        initialize_database()
        for path in sorted(DirectoryCsv.CONVERT.value.glob("*.csv")):
            ConvertTableImporter.execute(path)
        error_totalizer = ErrorTotalizer(DirectoryCsv.OUTPUT.value)
        for path_csv_file in sorted(DirectoryCsv.INPUT.value.glob("*.csv")):
            error_totalizer.convert_csv(path_csv_file)
        if error_totalizer.is_presented:
            error_totalizer.report_to_csv()
            raise SomeInvalidInputCsvError(error_totalizer.message)
