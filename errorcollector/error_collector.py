"""This module implements error collector."""
from abc import abstractmethod
from contextlib import ContextDecorator
from typing import List, TypeVar, Type, Optional, Generic


TypeVarError = TypeVar('TypeVarError', bound=Exception)


class ErrorCollector(ContextDecorator, Generic[TypeVarError]):
    """This class implements base methods of error collector."""
    def __init__(self, error_class: Type[TypeVarError], message: str):
        self.error_class = error_class
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            try:
                raise self.error_class(self.message) from exc_value
            except self.error_class as error:
                self.collect(error)
                return True
        return False

    @abstractmethod
    def collect(self, error: TypeVarError):
        """This method collects error into property."""


class SingleErrorCollector(ErrorCollector[TypeVarError]):
    """This class implements error collector for single error."""
    def __init__(self, error_class: Type[TypeVarError], message: str):
        super().__init__(error_class, message)
        self.error: Optional[TypeVarError] = None

    def collect(self, error: TypeVarError):
        self.error = error


class MultipleErrorCollector(ErrorCollector):
    """This class implements error collector for multiple error."""
    def __init__(self, error_class: Type[TypeVarError], message: str, list_error: List[TypeVarError]):
        super().__init__(error_class, message)
        self.list_error = list_error

    def collect(self, error: TypeVarError):
        self.list_error.append(error)
