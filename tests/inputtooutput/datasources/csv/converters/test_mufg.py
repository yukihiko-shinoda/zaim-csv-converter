"""Tests for MufgRowFactory."""
from dataclasses import dataclass

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.mufg import MufgRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import MufgRow


@dataclass
class Expected:
    """Expected values."""

    is_income: bool
    is_payment: bool
    is_transfer_income: bool
    is_transfer_payment: bool


class TestMufgRowFactory:
    """Tests for MufgRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @pytest.mark.parametrize(
        (
            "argument",
            "expected",
        ),
        [
            (
                InstanceResource.ROW_DATA_MUFG_INCOME_CARD,
                Expected(is_income=True, is_payment=False, is_transfer_income=False, is_transfer_payment=False),
            ),
            (
                InstanceResource.ROW_DATA_MUFG_PAYMENT,
                Expected(is_income=False, is_payment=True, is_transfer_income=False, is_transfer_payment=False),
            ),
            (
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT,
                Expected(is_income=False, is_payment=False, is_transfer_income=True, is_transfer_payment=False),
            ),
            (
                InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS,
                Expected(is_income=False, is_payment=False, is_transfer_income=False, is_transfer_payment=True),
            ),
        ],
    )
    @pytest.mark.usefixtures("database_session_stores_mufg")
    def test_create_success(self, argument: MufgRowData, expected: Expected) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        mufg_row = MufgRowFactory().create(argument)
        assert isinstance(mufg_row, MufgRow)
        self.assert_store_and_item(mufg_row, expected)

    def assert_store_and_item(self, mufg_row: MufgRow, expected: Expected) -> None:
        assert mufg_row.is_income == expected.is_income
        assert mufg_row.is_payment == expected.is_payment
        assert mufg_row.is_transfer_income == expected.is_transfer_income
        assert mufg_row.is_transfer_payment == expected.is_transfer_payment
