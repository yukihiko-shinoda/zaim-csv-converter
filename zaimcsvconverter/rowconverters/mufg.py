"""This module implements convert steps from MUFG input row to Zaim row."""
from abc import abstractmethod
from typing import Optional, Type

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats import ValidatedInputRow
from zaimcsvconverter.inputcsvformats.mufg import MufgRow
from zaimcsvconverter.rowconverters import ZaimIncomeRowConverter, ZaimPaymentRowConverter, ZaimTransferRowConverter, \
    ZaimRowConverterSelector, ZaimRowConverter


class MufgZaimIncomeRowConverter(ZaimIncomeRowConverter[MufgRow]):
    """This class implements convert steps from MUFG input row to Zaim income row."""
    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount_income(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        input_row = self.validated_input_row.input_row
        if input_row.deposit_amount is None:
            raise ValueError('Deposit amount on income row must be not None.')
        return input_row.deposit_amount


class MufgZaimPaymentRowConverter(ZaimPaymentRowConverter[MufgRow]):
    """This class implements convert steps from MUFG input row to Zaim payment row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        amount = self.validated_input_row.input_row.payed_amount
        if amount is None:
            raise ValueError('Payment amount on MUFG payment row must be not None.')
        return amount


class MufgZaimTransferRowConverter(ZaimTransferRowConverter[MufgRow]):
    """This class implements convert steps from MUFG input row to Zaim transfer row."""
    # @see https://github.com/PyCQA/pylint/issues/179
    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def _amount_transfer(self) -> int:
        if self._amount is None:
            raise ValueError('Transfer amount on MUFG transfer row must be not None.')
        return self._amount

    @property
    @abstractmethod
    def _amount(self) -> Optional[int]:
        """This property returns amount."""


class MufgAbstractIncomeZaimTransferRowConverter(MufgZaimTransferRowConverter):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""
    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        amount = self.validated_input_row.input_row.deposit_amount
        if amount is None:
            raise ValueError('Deposit amount on income row must be not None.')
        return amount


class MufgAbstractPaymentZaimTransferRowConverter(MufgZaimTransferRowConverter):
    """This class implements convert steps from MUFG payment input row to Zaim transfer row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def _cash_flow_target(self) -> str:
        """This property returns cash flow target."""

    @property
    def _amount(self) -> Optional[int]:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.validated_input_row.input_row.payed_amount


class MufgIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter):
    """This class implements convert steps from MUFG payment input row to Zaim transfer row."""
    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgTransferIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter):
    """This class implements convert steps from MUFG transfer income input row to Zaim transfer row."""
    @property
    def _cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.validated_input_row.store.transfer_target


class MufgTransferPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter):
    """This class implements convert steps from MUFG transfer payment input row to Zaim transfer row."""
    @property
    def _cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.validated_input_row.store.transfer_target


class MufgZaimRowConverterSelector(ZaimRowConverterSelector):
    """This class implements select steps from MUFG input row to Zaim row converter."""
    def select(self, validated_input_row: ValidatedInputRow[MufgRow]) -> Type[ZaimRowConverter]:
        input_row = validated_input_row.input_row
        if input_row.is_income and not input_row.is_by_card or \
           input_row.is_transfer_income and validated_input_row.store.transfer_target is None:
            return MufgZaimIncomeRowConverter
        if input_row.is_transfer_payment and validated_input_row.store.transfer_target is None:
            return MufgZaimPaymentRowConverter
        if input_row.is_income and input_row.is_by_card:
            return MufgIncomeZaimTransferRowConverter
        if input_row.is_payment:
            return MufgPaymentZaimTransferRowConverter
        if input_row.is_transfer_income and validated_input_row.store.transfer_target is not None:
            return MufgTransferIncomeZaimTransferRowConverter
        if input_row.is_transfer_payment and validated_input_row.store.transfer_target is not None:
            return MufgTransferPaymentZaimTransferRowConverter
        raise ValueError('Unsupported row. '
                         f'class = {type(input_row)}, is_by_card = {input_row.is_by_card}, '
                         f'store.transfer_target = {validated_input_row.store.transfer_target}')
