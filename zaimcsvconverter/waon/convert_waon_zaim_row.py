#!/usr/bin/env python


class ConvertWaonZaimRow(object):
    INDEX_STORE_WAON = 0
    INDEX_STORE_ZAIM = 1
    INDEX_CATEGORY_LARGE = 2
    INDEX_CATEGORY_SMALL = 3

    @property
    def store_waon(self):
        return self._store_waon

    @property
    def store_zaim(self):
        return self._store_zaim

    @property
    def category_large(self):
        return self._category_large

    @property
    def category_small(self):
        return self._category_small

    def __init__(self, row):
        self._store_waon = row[self.INDEX_STORE_WAON]
        self._store_zaim = row[self.INDEX_STORE_ZAIM]
        self._category_large = row[self.INDEX_CATEGORY_LARGE] if len(row) >= 3 else None
        self._category_small = row[self.INDEX_CATEGORY_SMALL] if len(row) >= 4 else None

    def convert_to_tuple(self):
        return self._store_waon, self._store_zaim, self._category_large, self._category_small
