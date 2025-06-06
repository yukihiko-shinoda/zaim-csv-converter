"""Converter from GOLD POINT CARD+ CSV data to record model version 201912."""

from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,  # noqa: H301,RUF100
)
from zaimcsvconverter.inputtooutput.datasources.csvfile.records.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,  # noqa: H301,RUF100
)


class GoldPointCardPlus201912RowFactory(InputRowFactory[GoldPointCardPlus201912RowData, GoldPointCardPlus201912Row]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance version 201912."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(  # type: ignore[override]
        self,
        input_row_data: GoldPointCardPlus201912RowData,
    ) -> GoldPointCardPlus201912Row:
        return GoldPointCardPlus201912Row(input_row_data)
