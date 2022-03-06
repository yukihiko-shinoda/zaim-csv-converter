"""Tests for mufg.py."""
from datetime import datetime

import pytest

from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.inputtooutput.datasources.csv.records.mufg import (
    MufgIncomeFromSelfRow,
    MufgPaymentToSelfRow,
    MufgStoreRow,
)
from zaimcsvconverter.models import Store


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
