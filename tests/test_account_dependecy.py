"""Tests for account_dependency.py ."""

from dataclasses import dataclass
from dataclasses import field

import pytest
from godslayer.god_slayer_factory import GodSlayerFactory

from zaimcsvconverter.account import AccountContext
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import WaonZaimRowConverterFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.waon import WaonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.waon import WaonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.waon import WaonRow


@dataclass
class Variables:
    """Variables for test."""

    regex_csv_file_name: str = r".*waon.*\.csv"
    god_slayer_factory: GodSlayerFactory = field(default_factory=GodSlayerFactory)
    input_row_data_class: type[WaonRowData] = WaonRowData
    input_row_factory: WaonRowFactory = field(default_factory=WaonRowFactory)
    zaim_row_factory_selector: WaonZaimRowConverterFactory = field(default_factory=WaonZaimRowConverterFactory)


@pytest.fixture(scope="class")
def created_account_context(variables: Variables) -> AccountContext[WaonRowData, WaonRow]:
    """Create account context."""
    return AccountContext(
        variables.regex_csv_file_name,
        variables.god_slayer_factory,
        variables.input_row_data_class,
        variables.input_row_factory,
        variables.zaim_row_factory_selector,
    )


@pytest.mark.parametrize("variables", [Variables()], scope="class")
class TestAccount:
    """Tests for account dependency."""

    def test_convert_string_to_int_or_none_1(
        self,
        # Reason: The pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        created_account_context: AccountContext[WaonRowData, WaonRow],
        variables: Variables,
    ) -> None:
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        assert created_account_context.regex_csv_file_name == variables.regex_csv_file_name

    def test_convert_string_to_int_or_none_2(
        self,
        # Reason: The pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        created_account_context: AccountContext[WaonRowData, WaonRow],
        variables: Variables,
    ) -> None:
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        assert created_account_context.god_slayer_factory == variables.god_slayer_factory

    def test_convert_string_to_int_or_none_3(
        self,
        # Reason: The pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        created_account_context: AccountContext[WaonRowData, WaonRow],
        variables: Variables,
    ) -> None:
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        assert created_account_context.input_row_data_class == variables.input_row_data_class

    def test_convert_string_to_int_or_none_4(
        self,
        # Reason: The pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        created_account_context: AccountContext[WaonRowData, WaonRow],
        variables: Variables,
    ) -> None:
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        assert created_account_context.input_row_factory == variables.input_row_factory

    def test_convert_string_to_int_or_none_5(
        self,
        # Reason: The pytest fixture. pylint: disable=unused-argument,redefined-outer-name
        created_account_context: AccountContext[WaonRowData, WaonRow],
        variables: Variables,
    ) -> None:
        """Argument should set into properties.

        Default encode should be UTF-8. Default csv herder should be None.
        """
        assert created_account_context.zaim_row_converter_factory == variables.zaim_row_factory_selector
