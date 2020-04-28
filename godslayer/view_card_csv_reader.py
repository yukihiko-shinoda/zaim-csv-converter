"""This module implements analyzing process of VIEW CARD CSV."""
import re
from pathlib import Path
from typing import Iterator, List, Generator

from godslayer.csv_reader import CsvReader
from godslayer.csv_with_header_reader import CsvWithHeaderReader
from godslayer.exceptions import InvalidHeaderError


class ViewCardCsvReader(CsvWithHeaderReader):
    def __init__(self, path_to_file: Path):
        super().__init__(
            path_to_file,
            [
                'ご利用年月日', 'ご利用箇所', 'ご利用額', '払戻額', 'ご請求額（うち手数料・利息）', '支払区分（回数）', '今回回数',
                '今回ご請求額・弁済金（うち手数料・利息）', '現地通貨額', '通貨略称', '換算レート'
            ],
            'shift_jis_2004'
        )

    def _process_csv(self, reader_input: Iterator[List[str]]) -> Generator[List[str], None, None]:
        if self.header:
            self._skip_header(reader_input)
        row = reader_input.__next__()
        if not bool(re.search(r'^\*{4}-\*{4}-\*{4}-[1-4]{4}\s.*$', row[0])):
            raise InvalidHeaderError('The column of card number and user name not found.')
        yield from CsvReader._process_csv(self, reader_input)
