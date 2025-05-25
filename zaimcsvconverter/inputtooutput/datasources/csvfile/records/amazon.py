"""This module implements row model of Amazon.co.jp CSV."""

from zaimcsvconverter import CONFIG
from zaimcsvconverter.file_csv_convert import FileCsvConvert
from zaimcsvconverter.inputtooutput.datasources.csvfile.data.amazon import AmazonRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputItemRow
from zaimcsvconverter.models import FileCsvConvertId
from zaimcsvconverter.models import Store
from zaimcsvconverter.models import StoreRowData


# pylint: disable=too-many-instance-attributes
class AmazonRow(InputItemRow[AmazonRowData]):
    """This class implements row model of Amazon.co.jp CSV."""

    def __init__(self, row_data: AmazonRowData) -> None:
        super().__init__(row_data, FileCsvConvert.AMAZON.value)
        self._store: Store = Store(
            FileCsvConvertId.AMAZON,
            StoreRowData("Amazon.co.jp", CONFIG.amazon.store_name_zaim),
        )
        self.price: int = row_data.price
        self.number: int = row_data.number

    @property
    def store(self) -> Store:
        return self._store
