"""Converter from GOLD POINT CARD+ CSV data to record model."""
from zaimcsvconverter.inputtooutput.datasources.csv.converters import InputRowFactory
from zaimcsvconverter.inputtooutput.datasources.csv.data.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputtooutput.datasources.csv.records.gold_point_card_plus import GoldPointCardPlusRow


class GoldPointCardPlusRowFactory(InputRowFactory[GoldPointCardPlusRowData, GoldPointCardPlusRow]):
    """This class implements factory to create GOLD POINT CARD+ CSV row instance."""

    # Reason: The example implementation of returns ignore incompatible return type.
    # see:
    #   - Create your own container — returns 0.18.0 documentation
    #     https://returns.readthedocs.io/en/latest/pages/create-your-own-container.html#step-5-checking-laws
    def create(self, input_row_data: GoldPointCardPlusRowData) -> GoldPointCardPlusRow:  # type: ignore[override]
        return GoldPointCardPlusRow(input_row_data)
