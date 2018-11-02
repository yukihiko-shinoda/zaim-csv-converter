#!/usr/bin/env python
import sys

from zaimcsvconverter.waon_csv_converter import WaonCsvConverter


def main(args):
    if len(args) != 2:
        raise ValueError(
            'Argument is not correct. Please specify convert source csv file. '
            + 'EX: python convert.py csvinput\waon201808.csv'
        )
    waon_csv_converter = WaonCsvConverter(args[1])
    waon_csv_converter.execute()


if __name__ == '__main__':
    main(sys.argv)
