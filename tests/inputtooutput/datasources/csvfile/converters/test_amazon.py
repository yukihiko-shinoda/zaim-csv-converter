"""Tests for AmazonRowFactory."""

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csvfile.converters.amazon import AmazonRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon import AmazonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.amazon import AmazonRow


class TestAmazonRowFactory:
    """Tests for AmazonRowFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(("argument", "expected"), [(InstanceResource.ROW_DATA_AMAZON_ECHO_DOT, AmazonRow)])
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_item")
    def test_create(argument: AmazonRowData, expected: type[AmazonRow]) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        gold_point_card_plus_row = AmazonRowFactory().create(argument)
        assert isinstance(gold_point_card_plus_row, expected)
