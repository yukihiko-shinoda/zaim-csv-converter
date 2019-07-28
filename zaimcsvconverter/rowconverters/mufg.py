"""This module implements convert steps from MUFG input row to Zaim row."""
from abc import abstractmethod, ABC
from typing import TypeVar

from zaimcsvconverter import CONFIG
from zaimcsvconverter.inputcsvformats.mufg import MufgStoreRow, MufgPaymentRow, MufgIncomeRow, MufgRow, \
    MufgPaymentToOthersRow, MufgIncomeFromOthersRow
from zaimcsvconverter.rowconverters import ZaimPaymentRowStoreConverter, ZaimTransferRowConverter, \
    ZaimRowConverterFactory, ZaimRowConverter, ZaimIncomeRowStoreConverter

TypeVarMufgRow = TypeVar('TypeVarMufgRow', bound=MufgRow)
TypeVarMufgIncomeRow = TypeVar('TypeVarMufgIncomeRow', bound=MufgIncomeRow)
TypeVarMufgPaymentRow = TypeVar('TypeVarMufgPaymentRow', bound=MufgPaymentRow)


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MufgZaimIncomeRowConverter(ZaimIncomeRowStoreConverter[MufgIncomeFromOthersRow]):
    """This class implements convert steps from MUFG input row to Zaim income row."""
    @property
    def cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.mufg.account_name

    @property
    def amount_income(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        input_row = self.input_row
        if input_row.deposit_amount is None:
            raise ValueError('Deposit amount on income row must be not None.')
        return input_row.deposit_amount


# Reason: Pylint's bug. pylint: disable=unsubscriptable-object
class MufgZaimPaymentRowConverter(ZaimPaymentRowStoreConverter[MufgPaymentToOthersRow]):
    """This class implements convert steps from MUFG input row to Zaim payment row."""
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.mufg.account_name

    @property
    def amount_payment(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        amount = self.input_row.payed_amount
        if amount is None:
            raise ValueError('Payment amount on MUFG payment row must be not None.')
        return amount


# Reason: Pylint's Bug. @see https://github.com/PyCQA/pylint/issues/179 pylint: disable=abstract-method
class MufgZaimTransferRowConverter(ZaimTransferRowConverter[TypeVarMufgRow], ABC):
    """This class implements convert steps from MUFG input row to Zaim transfer row."""


class MufgAbstractIncomeZaimTransferRowConverter(MufgZaimTransferRowConverter[TypeVarMufgIncomeRow]):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""
    @property
    @abstractmethod
    def cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.mufg.account_name

    @property
    def amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.deposit_amount


class MufgAbstractPaymentZaimTransferRowConverter(MufgZaimTransferRowConverter[TypeVarMufgPaymentRow]):
    """This class implements convert steps from MUFG payment input row [MufgPaymentRow]to Zaim transfer row."""
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        return CONFIG.mufg.account_name

    @property
    @abstractmethod
    def cash_flow_target(self) -> str:
        """This property returns cash flow target."""

    @property
    def amount_transfer(self) -> int:
        # Reason: Pylint's bug. pylint: disable=missing-docstring
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.payed_amount


class MufgIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter):
    """This class implements convert steps from MUFG income input row to Zaim transfer row."""
    @property
    def cash_flow_source(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter):
    """This class implements convert steps from MUFG payment input row to Zaim transfer row."""
    @property
    def cash_flow_target(self) -> str:
        return CONFIG.mufg.transfer_account_name


class MufgTransferIncomeZaimTransferRowConverter(MufgAbstractIncomeZaimTransferRowConverter[MufgIncomeFromOthersRow]):
    """This class implements convert steps from MUFG transfer income input row to Zaim transfer row."""
    @property
    def cash_flow_source(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.transfer_target


class MufgTransferPaymentZaimTransferRowConverter(MufgAbstractPaymentZaimTransferRowConverter[MufgPaymentToOthersRow]):
    """This class implements convert steps from MUFG transfer payment input row to Zaim transfer row."""
    @property
    def cash_flow_target(self) -> str:
        # Reason: Pylint's bug. pylint: disable=no-member
        return self.input_row.store.transfer_target


class MufgZaimRowConverterFactory(ZaimRowConverterFactory[MufgRow]):
    """This class implements select steps from MUFG input row to Zaim row converter."""
    def create(self, input_row: MufgRow) -> ZaimRowConverter:
        if input_row.is_payment:
            return MufgPaymentZaimTransferRowConverter(input_row)
        if input_row.is_income_from_other_own_account:
            return MufgIncomeZaimTransferRowConverter(input_row)
        if isinstance(input_row, MufgIncomeFromOthersRow) and input_row.is_transfer_income_from_other_own_account:
            return MufgTransferIncomeZaimTransferRowConverter(input_row)
        if input_row.is_income or input_row.is_transfer_income:
            return MufgZaimIncomeRowConverter(input_row)
        if isinstance(input_row, MufgPaymentToOthersRow) and input_row.is_transfer_payment_to_other_own_account:
            return MufgTransferPaymentZaimTransferRowConverter(input_row)
        if input_row.is_transfer_payment:
            return MufgZaimPaymentRowConverter(input_row)
        raise ValueError(self.build_message(input_row))

    @staticmethod
    def build_message(input_row: MufgRow) -> str:
        """This method builds error message."""
        message = ('Unsupported row. '
                   f'class = {type(input_row)}, '
                   f'is_income_from_other_own_account = {input_row.is_income_from_other_own_account}')
        if isinstance(input_row, MufgStoreRow):
            message = f'{message}, store.transfer_target = {input_row.store.transfer_target}'
        return message
