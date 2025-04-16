"""Zaim CSV Converter extended MUFG CSV Data model."""

from datetime import datetime

from pydantic.dataclasses import dataclass

from zaimcsvconverter.data import mufg
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputStoreRowData


@dataclass(config=dict(loc_by_alias=False))
# Reason: Model. pylint: disable=too-few-public-methods
class MufgRowData(mufg.MufgRowData, InputStoreRowData):
    """This class implements data class for wrapping list of MUFG CSV row model."""

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def store_name(self) -> str:
        return self.summary_content
