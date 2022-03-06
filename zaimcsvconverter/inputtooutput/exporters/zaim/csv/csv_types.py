"""We'll need a temporary file-like object, so use a tempfile.

see:
  - python - How to type-annotate object returned by csv.writer? - Stack Overflow
    https://stackoverflow.com/questions/51264355/how-to-type-annotate-object-returned-by-csv-writer
"""
# Reason: For typing.
import _csv  # noqa F401 pylint: disable=unused-import
from typing_extensions import TypeAlias

CSVReader: TypeAlias = "_csv._reader"
CSVWriter: TypeAlias = "_csv._writer"
