# Copyright (c) 2018 Yukihiko Shinoda
"""This module implements only calling Zaim CSV converter package."""

import sys

from zaimcsvconverter import PATH_FILE_CONFIG
from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def main() -> None:
    """Call Zaim CSV converter package."""
    if not PATH_FILE_CONFIG.is_file():
        print(
            f"Config file not found: {PATH_FILE_CONFIG}\n"
            "Copy config.yml.dist to config.yml and fill in your settings, then retry.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    ZaimCsvConverter.execute()


if __name__ == "__main__":
    main()
