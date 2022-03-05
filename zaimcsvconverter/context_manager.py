"""To implement context by using yield for class without calling any method.

see: python - entering context managers in __enter__ - Stack Overflow
https://stackoverflow.com/questions/47705573/entering-context-managers-in-enter
"""
from abc import ABC, abstractmethod
import contextlib
from types import TracebackType
from typing import Generic, Optional, TypeVar

TypeVarCovariant = TypeVar("TypeVarCovariant", covariant=True)


class ContextManager(Generic[TypeVarCovariant], ABC):
    """Class which can be used as `contextmanager`."""

    def __init__(self) -> None:
        self.__cm: Optional[contextlib._GeneratorContextManager[TypeVarCovariant]] = None

    # Reason: Maybe, there are no way to fix.
    # error: Argument 1 to "contextmanager" has incompatible type
    #   "Callable[[ContextManager[T_co]], _GeneratorContextManager[T_co]]";
    #   expected "Callable[[ContextManager[T_co]], Iterator[<nothing>]]"
    @abstractmethod  # type: ignore
    @contextlib.contextmanager
    def contextmanager(self) -> contextlib._GeneratorContextManager[TypeVarCovariant]:
        raise NotImplementedError("Abstract method")

    def __enter__(self) -> TypeVarCovariant:
        self.__cm = self.contextmanager()
        return self.__cm.__enter__()

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> bool | None:
        if self.__cm is None:
            return None
        return self.__cm.__exit__(exc_type, exc_value, traceback)
