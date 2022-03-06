"""Converter from GOLD POINT CARD+ CSV data to record model version 201912."""
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912RowData,
)
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912Row,
)


class GoldPointCardPlus201912RowFactory(InputRowFactory[GoldPointCardPlus201912RowData, GoldPointCardPlus201912Row]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance version 201912."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: GoldPointCardPlus201912RowData) -> GoldPointCardPlus201912Row:  # type: ignore
        return GoldPointCardPlus201912Row(input_row_data)
