"""This module implements only calling Zaim CSV converter package."""

from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def main() -> None:
    """This function calls Zaim CSV converter package."""
    ZaimCsvConverter.execute()


if __name__ == "__main__":
    main()
