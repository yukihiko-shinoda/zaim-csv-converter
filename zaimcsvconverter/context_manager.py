"""To implement context by using yield for class without calling any method.

see: python - entering context managers in __enter__ - Stack Overflow
https://stackoverflow.com/questions/47705573/entering-context-managers-in-enter
"""

import contextlib
from abc import ABC
from abc import abstractmethod
from types import TracebackType
from typing import Generic
from typing import Optional
from typing import TypeVar

TypeVarCovariant_co = TypeVar("TypeVarCovariant_co", covariant=True)


class ContextManager(Generic[TypeVarCovariant_co], ABC):
    """Class which can be used as `contextmanager`."""

    def __init__(self) -> None:
        self.__cm: Optional[contextlib._GeneratorContextManager[TypeVarCovariant_co]] = None

    @abstractmethod
    # Reason: Maybe, there are no way to fix.
    # error: Argument 1 to "contextmanager" has incompatible type
    #   "Callable[[ContextManager[T_co]], _GeneratorContextManager[T_co]]";  # noqa: ERA001
    #   expected "Callable[[ContextManager[T_co]], Iterator[<nothing>]]"
    @contextlib.contextmanager  # type: ignore[arg-type]
    def contextmanager(self) -> contextlib._GeneratorContextManager[TypeVarCovariant_co]:
        """This method is used to implement context manager."""
        raise NotImplementedError

    def __enter__(self) -> TypeVarCovariant_co:
        self.__cm = self.contextmanager()
        return self.__cm.__enter__()

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        if self.__cm is None:
            return None
        return self.__cm.__exit__(exc_type, exc_value, traceback)
