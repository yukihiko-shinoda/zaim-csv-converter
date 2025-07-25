"""MUFG CSV Data model."""

from enum import Enum

from pydantic.dataclasses import dataclass
from pydantictypes.string_to_datetime import StringSlashToDateTime
from pydantictypes.string_with_comma_to_optional_int import StrictStringWithCommaToOptionalInt

from zaimcsvconverter.first_form_normalizer import CsvRowData


class CashFlowKind(str, Enum):
    """This class implements constant of cash flow kind in MUFG CSV."""

    INCOME = "入金"
    PAYMENT = "支払い"
    TRANSFER_INCOME = "振替入金"
    TRANSFER_PAYMENT = "振替支払い"


@dataclass
# Reason: Model. pylint: disable=too-few-public-methods
class MufgRowData(CsvRowData):
    """This class implements data class for wrapping list of MUFG CSV row model."""

    # Reason: This implement depends on design of CSV. pylint: disable=too-many-instance-attributes
    class Summary(Enum):
        # Reason: Specification.
        CARD = "カ−ド"  # noqa: RUF001
        CARD_CONVENIENCE_STORE_ATM = "カードＣ１"
        YUCHO_BANK = "ゆうちょ"

    date_: StringSlashToDateTime
    summary: str
    summary_content: str
    payed_amount: StrictStringWithCommaToOptionalInt
    deposit_amount: StrictStringWithCommaToOptionalInt
    balance: str
    note: str
    is_uncapitalized: str
    cash_flow_kind: CashFlowKind
