"""This module implements convert steps from MUFG input row to Zaim row."""
from abc import abstractmethod
from typing import Type, TypeVar

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.mufg import MufgRow, MufgPaymentRow, MufgIncomeRow
from zaimcsvconverter.rowconverters import ZaimIncomeRowConverter, ZaimPaymentRowConverter, ZaimTransferRowConverter, \
    ZaimRowConverterSelector, ZaimRowConverter


TypeVarMufgRow = TypeVar('TypeVarMufgRow', bound=MufgRow)


class MufgZaimIncomeRowConverter(ZaimIncomeRowConverter[MufgIncomeRow]):
    """This class implements convert steps from MUFG input row to Zaim income row."""
    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount_income(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        input_row = self.input_row
        if input_row.deposit_amount is None:
            raise ValueError('Deposit amount on income row must be not None.')
        return input_row.deposit_amount


class MufgZaimPaymentRowConverter(ZaimPaymentRowConverter[MufgPaymentRow]):
    """This class implements convert steps from MUFG input row to Zaim payment row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        amount = self.input_row.payed_amount
        if amount is None:
            raise ValueError('Payment amount on MUFG payment row must be not None.')
        return amount


class MufgZaimTransferRowConverter(ZaimTransferRowConverter[TypeVarMufgRow]):
    """This class implements convert steps from MUFG input row to Zaim transfer row."""
    # @see https://github.com/PyCQA/pylint/issues/179
    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    @abstractmethod
    def _amount_transfer(self) -> int:
        """This property returns amount of transfer."""


class MufgAbstractIncomeZaimTransferRowConverter(MufgZaimTransferRowConverter[MufgIncomeRow]):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""
    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def _cash_flow_target(self) -> str:
        return CONFIG.mufg.account_name

    @property
    def _amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


class MufgAbstractPaymentZaimTransferRowConverter(MufgZaimTransferRowConverter[MufgPaymentRow]):
    """This class implements convert steps from MUFG payment input row [MufgPaymentRow]to Zaim transfer row."""
    @property
    def _cash_flow_source(self) -> str:
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def _cash_flow_target(self) -> str:
        """This property returns cash flow target."""

    @property
    def _amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


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
        return self.input_row.store.transfer_target


class MufgTransferPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter):
    """This class implements convert steps from MUFG transfer payment input row to Zaim transfer row."""
    @property
    def _cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.transfer_target


class MufgZaimRowConverterSelector(ZaimRowConverterSelector[MufgRow]):
    """This class implements select steps from MUFG input row to Zaim row converter."""
    def select(self, input_row: MufgRow) -> Type[ZaimRowConverter]:
        if input_row.is_payment:
            return MufgPaymentZaimTransferRowConverter
        if input_row.is_income and input_row.is_by_card:
            return MufgIncomeZaimTransferRowConverter
        if input_row.is_income or input_row.is_transfer_income and input_row.store.transfer_target is None:
            return MufgZaimIncomeRowConverter
        if input_row.is_transfer_income:
            return MufgTransferIncomeZaimTransferRowConverter
        if input_row.is_transfer_payment and input_row.store.transfer_target is None:
            return MufgZaimPaymentRowConverter
        if input_row.is_transfer_payment:
            return MufgTransferPaymentZaimTransferRowConverter
        raise ValueError('Unsupported row. '
                         f'class = {type(input_row)}, is_by_card = {input_row.is_by_card}, '
                         f'store.transfer_target = {input_row.store.transfer_target}')
