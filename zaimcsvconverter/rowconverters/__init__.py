"""This module implements convert steps from input row to Zaim row."""
from abc import abstractmethod
from typing import TypeVar, Generic, Type

from zaimcsvconverter.inputcsvformats import InputRow, ValidatedInputRow
from zaimcsvconverter.zaim_row import ZaimRow, ZaimIncomeRow, ZaimPaymentRow, ZaimTransferRow

TypeVarInputRow = TypeVar('TypeVarInputRow', bound=InputRow)


class ZaimRowConverter(Generic[TypeVarInputRow]):
    """This class implements convert steps from input row to Zaim row."""
    def __init__(self, validated_input_row: ValidatedInputRow[TypeVarInputRow]):
        self.validated_input_row: ValidatedInputRow[TypeVarInputRow] = validated_input_row

    @abstractmethod
    def convert(self) -> ZaimRow:
        """This method converts input row into zaim row."""


class ZaimIncomeRowConverter(ZaimRowConverter[TypeVarInputRow]):
    """This class implements convert steps from input row to Zaim income row."""
    def convert(self) -> ZaimIncomeRow:
        return ZaimIncomeRow(
            self.validated_input_row,
            self._cash_flow_target,
            self._amount_income,
        )

    @property
    @abstractmethod
    def _cash_flow_target(self) -> str:
        """This property returns income cash flow target."""

    @property
    @abstractmethod
    def _amount_income(self) -> int:
        """This property returns income amount income."""


class ZaimPaymentRowConverter(ZaimRowConverter[TypeVarInputRow]):
    """This class implements convert steps from input row to Zaim payment row."""
    def convert(self) -> ZaimPaymentRow:
        return ZaimPaymentRow(
            self.validated_input_row,
            self._cash_flow_source,
            self._note,
            self._amount_payment
        )

    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    def _note(self) -> str:
        return ZaimRow.NOTE_EMPTY

    @property
    @abstractmethod
    def _amount_payment(self) -> int:
        """This property returns amount payment."""


class ZaimTransferRowConverter(ZaimRowConverter[TypeVarInputRow]):
    """This class implements convert steps from input row to Zaim transfer row."""
    def convert(self) -> ZaimTransferRow:
        return ZaimTransferRow(
            self.validated_input_row,
            self._cash_flow_source,
            self._cash_flow_target,
            self._amount_transfer
        )

    @property
    @abstractmethod
    def _cash_flow_source(self) -> str:
        """This property returns cash flow source."""

    @property
    @abstractmethod
    def _cash_flow_target(self) -> str:
        """This property returns cash flow target."""

    @property
    @abstractmethod
    def _amount_transfer(self) -> int:
        """This property returns amount transfer."""


class ZaimRowConverterSelector:
    """This class implements select steps from input row to Zaim row converter."""
    def select(self, validated_input_row: ValidatedInputRow) -> Type[ZaimRowConverter]:
        """This method selects Zaim row converter."""
