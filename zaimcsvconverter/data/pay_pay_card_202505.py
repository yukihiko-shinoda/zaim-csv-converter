"""PayPay Card CSV Data model (2025-05 format)."""

from pydantic.dataclasses import dataclass
from pydantictypes.string_to_datetime import StringSlashToDateTime

from zaimcsvconverter.first_form_normalizer import CsvRowData


@dataclass
# Reason: Model, has similar designed versions.
# pylint: disable=too-few-public-methods,too-many-instance-attributes,duplicate-code
class PayPay202505RowData(CsvRowData):
    """This class implements data class for wrapping list of PayPay Card CSV row model (2025-05 format)."""

    used_cancelled_date: StringSlashToDateTime
    used_store_name_item_name: str
    user: str
    payment_method: str
    payment_kind: str
    used_amount: int
    commission: int
    total_payed_amount: int
    payment_amount_current_month: int
    balance_carried_forward_from_next_month: int
    adjustment_amount: int
    payment_date_current_month: StringSlashToDateTime
