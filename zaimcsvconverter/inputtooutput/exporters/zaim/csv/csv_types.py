"""We'll need a temporary file-like object, so use a tempfile.

see:
- python - How to type-annotate object returned by csv.writer? - Stack Overflow
  https://stackoverflow.com/questions/51264355/how-to-type-annotate-object-returned-by-csv-writer
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import _csv

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

# Reason: To conceal reference error for typing.
CSVReader: TypeAlias = _csv._reader  # noqa: SLF001 pylint: disable=protected-access,no-member
CSVWriter: TypeAlias = _csv._writer  # noqa: SLF001 pylint: disable=protected-access,no-member
