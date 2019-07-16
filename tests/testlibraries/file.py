"""This module implements fixtures and handlers about files."""
import os
import re
import sys
from pathlib import Path
from types import MethodType, FunctionType
from typing import Union, Type


def create_path_as_same_as_file_name(argument: Union[object, Type[object]]) -> Path:
    """This function creates and returns path as same as file name."""
    if not isinstance(argument, (MethodType, FunctionType)) and isinstance(argument, object):
        argument = argument.__class__
    matches = re.search(r'(.*)\.py', sys.modules[argument.__module__].__file__)
    if matches is None:
        raise ValueError("Can't get file name. Please check file name and extension.")
    return Path(matches.group(1))


def clean_up_directory(path_to_directory: Path) -> None:
    """This function cleans up content in specified directory."""
    for file in path_to_directory.rglob('*[!.gitkeep]'):
        os.unlink(str(file))
