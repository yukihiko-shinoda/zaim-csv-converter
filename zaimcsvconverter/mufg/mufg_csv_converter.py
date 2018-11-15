#!/usr/bin/env python

"""
This module implements converting steps for MUFG bank CSV.
"""

from pathlib import Path

from zaimcsvconverter.account_csv_converter import AccountCsvConverter
from zaimcsvconverter.mufg.mufg_income_row import MufgIncomeRow
from zaimcsvconverter.mufg.mufg_payment_row import MufgPaymentRow
from zaimcsvconverter.mufg.mufg_row import MufgRow, CashFlowKind, Index
from zaimcsvconverter.mufg.mufg_transfer_income_row import MufgTransferIncomeRow
from zaimcsvconverter.mufg.mufg_transfer_payment_row import MufgTransferPaymentRow


class MufgCsvConverter(AccountCsvConverter):
    """
    This class implements converting steps for MUFG bank CSV.
    """
    def __init__(self, csv_file: Path):
        super().__init__(csv_file, 'shift_jis_2004', True)

    @staticmethod
    def _create_account_row(list_row_account) -> MufgRow:
        cash_flow_kind = list_row_account[Index.CASH_FLOW_KIND.value]
        try:
            cash_flow_kind = CashFlowKind(cash_flow_kind)
        except ValueError as error:
            raise NotImplementedError(
                'The value of "Cash flow kind" has not been defined in this code. Cash flow kind =' + cash_flow_kind
            ) from error

        return {
            CashFlowKind.INCOME: MufgIncomeRow(list_row_account),
            CashFlowKind.PAYMENT: MufgPaymentRow(list_row_account),
            CashFlowKind.TRANSFER_INCOME: MufgTransferIncomeRow(list_row_account),
            CashFlowKind.TRANSFER_PAYMENT: MufgTransferPaymentRow(list_row_account)
        }.get(cash_flow_kind)
