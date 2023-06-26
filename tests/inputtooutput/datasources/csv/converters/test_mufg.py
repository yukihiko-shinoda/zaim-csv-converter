"""Tests for MufgRowFactory."""
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.converters.mufg import MufgRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import MufgRow


class TestMufgRowFactory:
    """Tests for MufgRowFactory."""

    # pylint: disable=unused-argument,too-many-arguments
    @staticmethod
    @pytest.mark.parametrize(
        (
            "argument",
            "expected_is_income",
            "expected_is_payment",
            "expected_is_transfer_income",
            "expected_is_transfer_payment",
        ),
        [
            (InstanceResource.ROW_DATA_MUFG_INCOME_CARD, True, False, False, False),
            (InstanceResource.ROW_DATA_MUFG_PAYMENT, False, True, False, False),
            (InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT, False, False, True, False),
            (InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS, False, False, False, True),
        ],
    )
    @pytest.mark.usefixtures("database_session_stores_mufg")
    def test_create_success(
        argument: MufgRowData,
        *,
        expected_is_income: bool,
        expected_is_payment: bool,
        expected_is_transfer_income: bool,
        expected_is_transfer_payment: bool,
    ) -> None:
        """Method should return Store model when note is defined."""
        # pylint: disable=protected-access
        mufg_row = MufgRowFactory().create(argument)
        assert isinstance(mufg_row, MufgRow)
        assert mufg_row.is_income == expected_is_income
        assert mufg_row.is_payment == expected_is_payment
        assert mufg_row.is_transfer_income == expected_is_transfer_income
        assert mufg_row.is_transfer_payment == expected_is_transfer_payment
