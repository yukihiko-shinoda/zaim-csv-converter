"""This module implements error handler."""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Iterator


class UndefinedContentErrorHandler:
    """This class implements undefined content error handler."""

    def __init__(self) -> None:
        self.list_error: list[list[str]] = []

    def __iter__(self) -> Iterator[list[str]]:
        return self.list_error.__iter__()

    def __len__(self) -> int:
        return len(self.list_error)

    def extend_list(self, error: list[list[str]]) -> None:
        """This method appends error list argument into error list property."""
        self.list_error.extend(error)
        self.uniquify()

    def extend(self, error_handler: UndefinedContentErrorHandler) -> None:
        """This method extends error list argument into error list property."""
        if not error_handler.is_presented:
            return
        error_handler.uniquify()
        self.list_error.extend(error_handler.list_error)
        self.uniquify()

    @property
    def is_presented(self) -> bool:
        """This property returns whether error is presented or not."""
        return bool(self.list_error)

    def uniquify(self) -> None:
        """This method uniquify error list."""
        # noinspection PyTypeChecker
        self.list_error = np.unique(np.array(self.list_error), axis=0).tolist()
