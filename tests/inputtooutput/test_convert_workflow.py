"""Tests for input_csv.py."""
from pathlib import Path
from typing import Any

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import Account, AccountContext
from zaimcsvconverter.exceptions.invalid_input_csv_error import InvalidInputCsvError
from zaimcsvconverter.exceptions import InvalidCellError
from zaimcsvconverter.inputtooutput.convert_workflow import ConvertWorkflow
from zaimcsvconverter.inputtooutput.converters.recordtozaim.record_to_zaim_converter import RecordToZaimConverter
from zaimcsvconverter.inputtooutput.datasources.csv import Csv
from zaimcsvconverter.inputtooutput.datasources.csv.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.exporters.zaim.csv.zaim_csv_output_exporter import ZaimCsvOutputModelExporter


class TestConvertWorkflow:
    """Tests for InputData."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        "database_session_with_schema, path_file_csv_input",
        [([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO], "waon")],
        indirect=["database_session_with_schema", "path_file_csv_input"],
    )
    @pytest.mark.usefixtures("yaml_config_load", "database_session_with_schema")
    def test(path_file_csv_input: Path, tmp_path: Path) -> None:
        """Tests following:

        - InvalidInputCsvError should be raised
          when there are row having store name which there are no data in convert table.
        - Input CSV should be invalid
          when there are row having store name which there are no data in convert table.
        - Invalid row dictionary should store InvalidRowError
          when there are row having store name which there are no data in convert table.
        - Undefined content error handler should be empty.
        """
        account_context: AccountContext[Any, Any] = Account.create_by_path_csv_input(path_file_csv_input).value
        god_slayer = account_context.god_slayer_factory.create(path_file_csv_input)
        csv_record_processor = CsvRecordProcessor(
            account_context.input_row_data_class, account_context.input_row_factory
        )
        data_source = Csv(god_slayer, csv_record_processor)
        record_converter = RecordToZaimConverter(account_context.zaim_row_converter_factory)
        output_model_exporter = ZaimCsvOutputModelExporter(tmp_path / "test.csv")
        convert_workflow = ConvertWorkflow(data_source, record_converter, output_model_exporter)
        with pytest.raises(InvalidInputCsvError) as error:
            convert_workflow.execute()
        assert str(error.value) == (
            "Undefined store or item name in convert table CSV exists in test_waon.csv. "
            "Please check property AccountCsvConverter.list_undefined_store."
        )
        assert data_source.is_invalid
        invalid_row_error = data_source.dictionary_invalid_record[0][0]
        assert isinstance(invalid_row_error, InvalidCellError)
        assert str(invalid_row_error) == "Charge kind in charge row is required. Charge kind = -"
        assert not data_source.undefined_content_error_handler.is_presented
