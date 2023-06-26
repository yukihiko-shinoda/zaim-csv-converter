"""This module implements row model of PayPal CSV.

see:
  - PayPal activity download specification
    https://www.paypalobjects.com/webstatic/en_US/developer/docs/pdf/PP_ActivityDownload.pdf
"""
from zaimcsvconverter.data.pay_pal import BalanceImpact, Status
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csv.data.pay_pal import PayPalRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records import InputStoreItemRow


class PayPalRow(InputStoreItemRow[PayPalRowData]):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: PayPalRowData) -> None:
        super().__init__(row_data, FileCsvConvert.PAY_PAL_STORE.value, FileCsvConvert.PAY_PAL_ITEM.value)
        self.status: Status = row_data.status
        self.gross: int = row_data.gross
        self.fee: int = row_data.fee
        self.net: int = row_data.net
        self.balance_impact: BalanceImpact = row_data.balance_impact

    @property
    def validate(self) -> bool:
        self.stock_error(
            self.check_net_is_gross_plus_fee,
            f"Net is not gross + fee. Net: {self.net}, gross: {self.gross}, fee: {self.fee}",
        )
        return super().validate

    def check_net_is_gross_plus_fee(self) -> None:
        if self.net != self.gross + self.fee:
            raise ValueError

    @property
    def is_row_to_skip(self) -> bool:
        return not self.is_completed or self.is_debit or self.is_memo

    @property
    def is_completed(self) -> bool:
        return self.status == Status.COMPLETED

    @property
    def is_debit(self) -> bool:
        return self.balance_impact == BalanceImpact.DEBIT

    @property
    def is_memo(self) -> bool:
        return self.balance_impact == BalanceImpact.MEMO
