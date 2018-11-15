#!/usr/bin/env python

"""
This module implements only calling Zaim CSV converter package.
"""
from typing import NoReturn

from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def main() -> NoReturn:
    """
    This function calls Zaim CSV converter package.
    """
    zaim_csv_converter = ZaimCsvConverter()
    zaim_csv_converter.execute()


if __name__ == '__main__':
    main()
