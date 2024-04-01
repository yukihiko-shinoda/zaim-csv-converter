"""PayPay Card CSV Data model."""

from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringSlashToDateTime
from zaimcsvconverter.first_form_normalizer import CsvRowData


# Reason: Model. pylint: disable=too-few-public-methods,too-many-instance-attributes
@dataclass
class PayPayRowData(CsvRowData):
    """This class implements data class for wrapping list of PayPay Card CSV row model."""

    used_cancelled_date: StringSlashToDateTime
    used_store_name_item_name: str
    user: str
    payment_kind: str
    used_amount: int
    commission: int
    total_payed_amount: int
    payment_amount_current_month: int
    balance_carried_forward_from_next_month: int
    adjustment_amount: int
    payment_date_current_month: StringSlashToDateTime
