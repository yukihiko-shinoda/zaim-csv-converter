"""Type aliases for the reader and writer objects returned by csv.reader() and csv.writer().

Typeshed defines these as public ``_csv.Reader`` / ``_csv.Writer`` classes (CPython 3.12+ also
exposes them at runtime, though these aliases are never evaluated at runtime).

see:
- python - How to type-annotate object returned by csv.writer? - Stack Overflow
  https://stackoverflow.com/questions/51264355/how-to-type-annotate-object-returned-by-csv-writer
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Reason: Ruff sees the usage inside the string aliases below, but Flake8 doesn't (hence F401),
    #         and Ruff would then flag the noqa itself as unused (hence RUF100).
    import _csv  # noqa: F401,RUF100
    from typing import TypeAlias

# Reason: String forward references, since _csv is imported only under TYPE_CHECKING.
CSVReader: TypeAlias = "_csv.Reader"
CSVWriter: TypeAlias = "_csv.Writer"
