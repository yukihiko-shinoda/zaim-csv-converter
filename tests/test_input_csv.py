"""Tests for input_csv.py."""
import csv
from pathlib import Path

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.exceptions import InvalidInputCsvError, InvalidRowError
from zaimcsvconverter.input_csv import InputCsv


class TestInputCsv:
    """Tests for InputCsv."""
    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        'database_session_with_schema, path_file_csv_input', [
            ([InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO], 'waon')
        ], indirect=['database_session_with_schema', 'path_file_csv_input'])
    def test(yaml_config_load, database_session_with_schema, path_file_csv_input: Path, tmp_path):
        """
        InvalidInputCsvError should be raised
          when there are row having store name which there are no data in convert table.
        Input CSV should be invalid
          when there are row having store name which there are no data in convert table.
        Invalid row dictionary should store InvalidRowError
          when there are row having store name which there are no data in convert table.
        Undefined content error handler should be empty.
        """
        input_csv = InputCsv(path_file_csv_input)
        with (tmp_path / 'test.csv').open('w', encoding='UTF-8', newline='\n') as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            with pytest.raises(InvalidInputCsvError) as error:
                input_csv.covert_to_zaim(writer_zaim)
        assert str(error.value) == ('Undefined store name in convert table CSV exists in test_waon.csv. '
                                    'Please check property AccountCsvConverter.list_undefined_store.')
        assert input_csv.is_invalid
        invalid_row_error = input_csv.dictionary_invalid_row[0][0]
        assert isinstance(invalid_row_error, InvalidRowError)
        assert str(invalid_row_error) == 'Charge kind in charge row is required. Charge kind = ChargeKind.NULL'
        assert not input_csv.undefined_content_error_handler.is_presented
