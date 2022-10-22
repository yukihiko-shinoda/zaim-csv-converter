"""PayPay Card CSV Data model."""
from pydantic.dataclasses import dataclass

from zaimcsvconverter.customdatatypes.string_to_datetime import StringNumberOnlyToDateTime
from zaimcsvconverter.customdatatypes.yen_string_to_int import StrictYenStringToInt
from zaimcsvconverter.first_form_normalizer import CsvRowData


# Reason: Model. pylint: disable=too-few-public-methods,too-many-instance-attributes
@dataclass
class PayPayRowData(CsvRowData):
    """This class implements data class for wrapping list of PayPay Card CSV row model."""

    used_date: StringNumberOnlyToDateTime
    used_store_name_item_name: str
    user: str
    payment_kind: str
    used_amount: StrictYenStringToInt
    commission: StrictYenStringToInt
    total_payed_amount: StrictYenStringToInt
    payment_amount_current_month: StrictYenStringToInt
    balance_carried_forward_from_next_month: StrictYenStringToInt
