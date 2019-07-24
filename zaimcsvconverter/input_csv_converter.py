"""This module implements abstract converting steps for CSV."""
import csv
from pathlib import Path

from zaimcsvconverter.account import Account
from zaimcsvconverter import DirectoryCsv
from zaimcsvconverter.error_handler import ErrorHandler
from zaimcsvconverter.exceptions import InvalidRowError
from zaimcsvconverter.zaim_row import ZaimRow


class InputCsvConverter:
    """This class implements abstract converting steps for CSV."""
    def __init__(self, path_csv_file: Path, directory_csv_output: Path = DirectoryCsv.OUTPUT.value):
        self._path_csv_file = path_csv_file
        self.directory_csv_output = directory_csv_output
        self._account = Account.create_by_path_csv_input(path_csv_file)
        self.error_handler: ErrorHandler = ErrorHandler()

    def execute(self) -> None:
        """This method executes CSV convert steps."""
        with (self.directory_csv_output / self._path_csv_file.name).open(
                'w', encoding='UTF-8', newline='\n'
        ) as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            writer_zaim.writerow(ZaimRow.HEADER)
            self._convert_from_account(writer_zaim)

    def _convert_from_account(self, writer_zaim) -> None:
        account_dependency = self._account.value
        with self._path_csv_file.open('r', encoding=account_dependency.encode) as file_input:
            reader_input = csv.reader(file_input)
            if account_dependency.csv_header:
                try:
                    while reader_input.__next__() != account_dependency.csv_header:
                        pass
                except StopIteration as error:
                    raise StopIteration(
                        f'{self._path_csv_file.name} doesn\'t include header row.'
                        + 'Please confirm AccountConfig.csv_header. '
                        + f'AccountConfig.csv_header = {account_dependency.csv_header}'
                    ) from error
            self._iterate_convert(reader_input, writer_zaim)

    def _iterate_convert(self, reader_input, writer_zaim) -> None:
        for list_input_row_standard_type_value in reader_input:
            input_row_data = self._account.create_input_row_data_instance(list_input_row_standard_type_value)
            input_row = self._account.create_input_row_instance(input_row_data)
            try:
                validated_input_row = input_row.validate()
            except InvalidRowError:
                self.error_handler.append_undefined_content(self._account.value.file_name_csv_convert, input_row_data)
                continue
            if validated_input_row.is_row_to_skip:
                continue
            converter = self._account.value.zaim_row_converter_selector.select(validated_input_row)
            zaim_row = converter(validated_input_row).convert()
            list_row_zaim = zaim_row.convert_to_list()
            writer_zaim.writerow(list_row_zaim)
        if self.error_handler.is_presented:
            self.error_handler.uniquify()
            raise KeyError(
                f'Undefined store name in convert table CSV exists in {self._path_csv_file.name}.'
                + 'Please check property AccountCsvConveter.list_undefined_store.'
            )
