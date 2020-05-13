"""Tests for input_csv.py."""
import csv
from pathlib import Path

import pytest

from godslayer.exceptions import InvalidRecordError
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.account import Account
from zaimcsvconverter.datasources.csv import Csv
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.input_csv import InputData


class TestInputCsv:
    """Tests for InputData."""
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
        account = Account.create_by_path_csv_input(path_file_csv_input)
        csv_reader = Csv(account.value.god_slayer_factory.create(path_file_csv_input))
        input_data = InputData(csv_reader, account)
        with (tmp_path / 'test.csv').open('w', encoding='UTF-8', newline='\n') as file_zaim:
            writer_zaim = csv.writer(file_zaim)
            with pytest.raises(InvalidInputCsvError) as error:
                input_data.export_as_zaim_csv(writer_zaim)
        assert str(error.value) == ('Undefined store name in convert table CSV exists in test_waon.csv. '
                                    'Please check property AccountCsvConverter.list_undefined_store.')
        assert input_data.data_source.is_invalid
        invalid_row_error = input_data.data_source.dictionary_invalid_record[0][0]
        assert isinstance(invalid_row_error, InvalidRecordError)
        assert str(invalid_row_error) == 'Charge kind in charge row is required. Charge kind = ChargeKind.NULL'
        assert not input_data.undefined_content_error_handler.is_presented
