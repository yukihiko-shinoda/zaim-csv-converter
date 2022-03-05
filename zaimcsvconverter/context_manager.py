from abc import ABC, abstractmethod
import contextlib


class ContextManager(ABC):
  """Class which can be used as `contextmanager`."""

  def __init__(self):
    self.__cm = None

  @abstractmethod
  @contextlib.contextmanager
  def contextmanager(self):
    raise NotImplementedError('Abstract method')

  def __enter__(self):
    self.__cm = self.contextmanager()
    return self.__cm.__enter__()

  def __exit__(self, exc_type, exc_value, traceback):
    return self.__cm.__exit__(exc_type, exc_value, traceback)