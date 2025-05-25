"""Provides fixtures for tests of zaimcsvconverter.inputtooutput.exporters.zaim.csv."""

from pathlib import Path

import pytest

from tests.testlibraries.row_data import ZaimRowData
from zaimcsvconverter.accounts.enum import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.csv_record_processor import CsvRecordProcessor
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputRow


@pytest.fixture(scope="class")
def zaim_row_data_created_by_zaim_row(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_item_class_scope: None,  # noqa: ARG001
    account: Account,
    input_row_data: InputRowData,
) -> ZaimRowData:
    """Creates ZaimRowData instance by ZaimRow."""
    csv_record_processor = CsvRecordProcessor(account.value.input_row_factory)
    input_row = csv_record_processor.create_input_row_instance(input_row_data)
    # Reason: Pylint's bug. pylint: disable=no-member
    zaim_low = ZaimRowFactory.create(account.value.zaim_row_converter_factory.create(input_row, Path()))
    list_zaim_row = zaim_low.convert_to_list()
    return ZaimRowData(*list_zaim_row)


@pytest.fixture(scope="class")
def zaim_row_data_created_by_zaim_payment_row(
    _yaml_config_load_class_scope: None,
    # Reason: pytest fixture can't use pytest.mark.usefixtures. pylint: disable=unused-argument
    database_session_stores_item_class_scope: None,  # noqa: ARG001
    input_row_factory: InputRowFactory[InputRowData, InputRow[InputRowData]],
    input_row_data: InputRowData,
    zaim_row_converter_factory: CsvRecordToZaimRowConverterFactory[InputRow[InputRowData], InputRowData],
) -> ZaimRowData:
    """Creates ZaimRowData instance by ZaimPaymentRow."""
    input_row = input_row_factory.create(input_row_data)
    zaim_low = ZaimRowFactory.create(zaim_row_converter_factory.create(input_row, Path()))
    list_zaim_row = zaim_low.convert_to_list()
    return ZaimRowData(*list_zaim_row)
