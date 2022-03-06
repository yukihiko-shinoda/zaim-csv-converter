"""Tests for mufg.py."""
from datetime import datetime

from pydantic import ValidationError
import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.data.mufg import CashFlowKind
from zaimcsvconverter.inputtooutput.datasources.csv.data.mufg import MufgRowData
from zaimcsvconverter.inputtooutput.datasources.csv.data import RowDataFactory
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import (
    MufgIncomeFromSelfRow,
    MufgPaymentToSelfRow,
    MufgStoreRow,
)
from zaimcsvconverter.models import Store


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
            ]
        )
        assert mufg_row_data.summary == summary
        assert mufg_row_data.payed_amount == 3628
        assert mufg_row_data.deposit_amount is None
        assert mufg_row_data.balance == balance
        assert mufg_row_data.note == note
        assert mufg_row_data.is_uncapitalized == is_uncapitalized
        assert mufg_row_data.cash_flow_kind == CashFlowKind.TRANSFER_PAYMENT
        assert mufg_row_data.date == datetime(2018, 11, 28, 0, 0)
        assert mufg_row_data.store_name == summary_content

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("database_session_stores_mufg")
    def test_create_fail() -> None:
        """Method should raise ValueError when note is not defined."""
        with pytest.raises(ValidationError) as excinfo:
            # pylint: disable=protected-access
            RowDataFactory(MufgRowData).create(InstanceResource.ROW_DATA_MUFG_UNSUPPORTED_NOTE)
        errors = excinfo.value.errors()
        assert len(errors) == 1
        error = errors[0]
        assert error["loc"] == ("cash_flow_kind",)
        assert error["msg"] == "value is not a valid enumeration member; permitted: '入金', '支払い', '振替入金', '振替支払い'"


class TestMufgIncomeRow:
    """Tests for MufgIncomeRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_init() -> None:
        """Arguments should set into properties."""
        mufg_row = MufgStoreRow(InstanceResource.ROW_DATA_MUFG_INCOME_CARD)
        assert mufg_row.date == datetime(2018, 10, 1, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim is None


class TestMufgPaymentRow:
    """Tests for MufgPaymentRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_init() -> None:
        """Arguments should set into properties."""
        mufg_row = MufgStoreRow(InstanceResource.ROW_DATA_MUFG_PAYMENT)
        assert mufg_row.date == datetime(2018, 11, 5, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim is None


class TestMufgIncomeFromSelfRow:
    """Tests for MufgIncomeFromSelfRow."""

    @staticmethod
    def test_deposit_amount_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            MufgIncomeFromSelfRow(InstanceResource.ROW_DATA_MUFG_PAYMENT).deposit_amount
        assert str(error.value) == "Deposit amount on income row is not allowed empty."


class TestMufgPaymentToSelfRow:
    """Tests for MufgPaymentToSelfRow."""

    @staticmethod
    def test_payed_amount_fail() -> None:
        """Property should raise ValueError when value is None."""
        with pytest.raises(ValueError) as error:
            # pylint: disable=expression-not-assigned
            # noinspection PyStatementEffect
            MufgPaymentToSelfRow(InstanceResource.ROW_DATA_MUFG_INCOME_CARD).payed_amount
        assert str(error.value) == "Payed amount on payment row is not allowed empty."


class TestMufgTransferIncomeRow:
    """Tests for MufgTransferIncomeRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_init() -> None:
        """Arguments should set into properties."""
        store_name = "三菱UFJ銀行"
        mufg_row = MufgStoreRow(InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT)
        assert mufg_row.date == datetime(2018, 8, 20, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim == store_name


class TestMufgTransferPaymentRow:
    """Tests for MufgTransferPaymentRow."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.usefixtures("yaml_config_load", "database_session_stores_mufg")
    def test_init() -> None:
        """Arguments should set into properties."""
        store_name = "東京都水道局　経理部管理課"
        mufg_row = MufgStoreRow(InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS)
        assert mufg_row.date == datetime(2018, 11, 28, 0, 0, 0)
        assert isinstance(mufg_row.store, Store)
        assert mufg_row.store.name_zaim == store_name
