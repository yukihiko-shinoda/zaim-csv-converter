"""Tests for mufg.py."""

from datetime import datetime

from pydantic import ValidationError
import pytest

from tests.testlibraries.assert_list import assert_each_properties
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.data.mufg import CashFlowKind
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import RowDataFactory


class TestMufgRowData:
    """Tests for MufgRowData."""

    @staticmethod
    def test_init_and_property() -> None:
        """Tests following:

        - Property date should return datetime object.
        - Property store_date should return used_store.
        """
        date = "2018/11/28"
        summary = "水道"
        summary_content = "トウキヨウトスイドウ"
        payed_amount = "3628"
        deposit_amount = ""
        balance = "5000000"
        note = ""
        is_uncapitalized = ""
        cash_flow_kind = "振替支払い"
        expected_payed_amount = 3628
        mufg_row_data = RowDataFactory(MufgRowData).create(
            [
                date,
                summary,
                summary_content,
                payed_amount,
                deposit_amount,
                balance,
                note,
                is_uncapitalized,
                cash_flow_kind,
            ],
        )
        assert_each_properties(
            mufg_row_data,
            [
                # Reason: Time is not used in this process.
                datetime(2018, 11, 28, 0, 0),  # noqa: DTZ001
                summary,
                summary_content,
                expected_payed_amount,
                None,
                balance,
                note,
                is_uncapitalized,
                CashFlowKind.TRANSFER_PAYMENT,
            ],
        )

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_stores_mufg")
    def test_create_fail() -> None:
        """Method should raise ValueError when note is not defined."""
        # - The key: `loc` of ValidationError should be not index but property name even if instantiate dataclass without kwarg? · Issue #9140 · pydantic/pydantic  # noqa: E501  # pylint: disable=line-too-long
        #   https://github.com/pydantic/pydantic/issues/9140
        index_cash_flow_kind = 8
        with pytest.raises(ValidationError) as excinfo:
            # pylint: disable=protected-access
            RowDataFactory(MufgRowData).create(InstanceResource.ROW_DATA_MUFG_UNSUPPORTED_NOTE)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == (index_cash_flow_kind,)
        assert error["msg"] == "".join(
            ["Input should be '入金', '支払い', '振替入金' or '振替支払い'"],
        )
