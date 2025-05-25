"""Tests for input_csv.py."""

from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.accounts.enum import Account
from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError
from zaimcsvconverter.first_form_normalizer import FirstFormNormalizer
from zaimcsvconverter.inputtooutput.convert_workflow import ConvertWorkflow
from zaimcsvconverter.inputtooutput.converters.recordtozaim.record_to_zaim_converter import RecordToZaimConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_file import Csv
from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.csvfile.zaim_csv_output_exporter import ZaimCsvOutputModelExporter

if TYPE_CHECKING:
    from zaimcsvconverter.accounts.context import AccountContext


class TestConvertWorkflow:
    """Tests for InputData."""

    @pytest.mark.parametrize(
        ("database_session_with_schema", "path_file_csv_input"),
        [([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO], "waon")],
        indirect=["database_session_with_schema", "path_file_csv_input"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test(self, path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - InvalidInputCsvError should be raised
          when there are record having store name which there are no data in convert table.
        - Input CSV should be invalid
          when there are record having store name which there are no data in convert table.
        - Invalid record dictionary should store InvalidCellError
          when there are record having store name which there are no data in convert table.
        - Undefined content error handler should be empty.
        """
        account_context: AccountContext[Any, Any] = Account.create_by_path_csv_input(path_file_csv_input).value
        god_slayer = account_context.god_slayer_factory.create(path_file_csv_input)
        first_form_normalizer = FirstFormNormalizer(god_slayer, account_context.input_row_data_class)
        csv_record_processor = CsvRecordProcessor(account_context.input_row_factory)
        data_source = Csv(first_form_normalizer, csv_record_processor)
        record_converter = RecordToZaimConverter(account_context.zaim_row_converter_factory, path_file_csv_input)
        output_model_exporter = ZaimCsvOutputModelExporter(tmp_path / "test.csv")
        convert_workflow = ConvertWorkflow(data_source, record_converter, output_model_exporter)
        with pytest.raises(InvalidInputCsvError) as error:
            convert_workflow.execute()
        assert str(error.value) == (
            "Undefined store or item name in convert table CSV exists in test_waon.csv. "
            "Please check property AccountCsvConverter.list_undefined_store."
        )
        self.assert_data_source(data_source)

    def assert_data_source(self, data_source: Csv[Any, Any]) -> None:
        assert data_source.is_invalid
        invalid_cell_error = data_source.dictionary_invalid_record[0][0]
        assert isinstance(invalid_cell_error, InvalidCellError)
        assert str(invalid_cell_error) == "Charge kind in charge row is required. Charge kind = -"
        assert not data_source.undefined_content_error_handler.is_presented
