#!/usr/bin/env python
import sqlite3
from contextlib import contextmanager, ExitStack
from typing import NoReturn, Optional

from zaimcsvconverter.waon.convert_waon_zaim_row import ConvertWaonZaimRow


class DatabaseWrapper(object):
    def __init__(self):
        self._connection = sqlite3.connect(':memory:')

    @contextmanager
    def _close_on_error(self):
        with ExitStack() as stack:
            stack.push(self)
            yield
            stack.pop_all()

    def __enter__(self):
        with self._close_on_error():
            # noinspection SqlNoDataSourceInspection,SqlResolve,SqlDialectInspection
            self._connection.execute('create table convert_waon_zaim(store_waon text UNIQUE, store_zaim text, category_large text, category_small text)')
        return self

    def save_convert_waon_zaim(self, convert_waon_zaim_row: ConvertWaonZaimRow) -> NoReturn:
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        sql = 'insert into convert_waon_zaim (store_waon, store_zaim, category_large, category_small) values (?, ?, ?, ?)'
        self._connection.execute(sql, convert_waon_zaim_row.convert_to_tuple())

    def find_convert_waon_zaim(self, store_waon: str) -> Optional[ConvertWaonZaimRow]:
        cur = self._connection.cursor()
        # noinspection SqlNoDataSourceInspection,SqlDialectInspection
        cur.execute('select * from convert_waon_zaim where store_waon=?', (store_waon,))
        record = cur.fetchone()
        if record is None:
            return None
        convert_waon_zaim_row = ConvertWaonZaimRow(record)
        cur.close()
        return convert_waon_zaim_row

    def __exit__(self, *exc):
        self._connection.close()
