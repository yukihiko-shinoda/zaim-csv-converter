"""WAON CSV Data model."""

from enum import Enum

from pydantic.dataclasses import dataclass

from pydantictypes.kanji_yen_string_to_int import StrictKanjiYenStringToInt
from pydantictypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


class UseKind(str, Enum):
    """This class implements constant of user kind in WAON CSV."""

    PAYMENT = "支払"
    PAYMENT_CANCEL = "支払取消"
    CHARGE = "チャージ"
    AUTO_CHARGE = "オートチャージ"
    DOWNLOAD_POINT = "ポイントダウンロード"
    # Reason: Specification.
    TRANSFER_WAON_UPLOAD = "WAON移行（アップロード）"  # noqa: RUF001
    TRANSFER_WAON_DOWNLOAD = "WAON移行（ダウンロード）"  # noqa: RUF001

    # Reason: Python 3.11 displays not string of value but name of value. pylint: disable=useless-parent-delegation
    def __str__(self) -> str:
        return super().__str__()


class ChargeKind(str, Enum):
    """This class implements constant of charge kind in WAON CSV."""

    BANK_ACCOUNT = "銀行口座"
    POINT = "ポイント"
    CASH = "現金"
    CREDIT_CARD = "クレジット"
    DOWNLOAD_VALUE = "バリューダウンロード"
    NULL = "-"

    # Reason: Python 3.11 displays not string of value but name of value. pylint: disable=useless-parent-delegation
    def __str__(self) -> str:
        return super().__str__()


# Reason: Model. pylint: disable=too-few-public-methods
@dataclass
class WaonRowData(CsvRowData):
    """This class implements data class for wrapping list of WAON CSV row model."""

    date_: StringSlashToDateTime
    used_store: str
    used_amount: StrictKanjiYenStringToInt
    use_kind: UseKind
    charge_kind: ChargeKind
