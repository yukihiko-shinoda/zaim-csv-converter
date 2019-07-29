"""This module implements utility class about file."""
import re
import sys
from pathlib import Path
from types import MethodType, FunctionType

from tests.testlibraries.instance_resource import InstanceResource


class FilePathUtility:
    """This class implements utility method about file."""
    @classmethod
    def create_path_as_same_as_file_name(cls, argument: object) -> Path:
        """This method creates and returns path as same as file name."""
        if not isinstance(argument, (MethodType, FunctionType)) and isinstance(argument, object):
            argument = argument.__class__
        matches = re.search(r'(.*)\.py', sys.modules[argument.__module__].__file__)
        if matches is None:
            raise ValueError("Can't get file name. Please check file name and extension.")
        return Path(matches.group(1))

    @classmethod
    def create_path_to_resource_directory(cls, argument: object) -> Path:
        """This method creates path to test resource directory."""
        path_as_same_as_file_name = cls.create_path_as_same_as_file_name(argument)
        return InstanceResource.PATH_TEST_RESOURCES / path_as_same_as_file_name.relative_to(InstanceResource.PATH_TESTS)

    @classmethod
    def get_config_file_path(cls, request) -> Path:
        """This method build file path if file name is presented by parametrize."""
        if hasattr(request, 'param'):
            return cls.create_path_to_resource_directory(request.function) / request.param
        return InstanceResource.PATH_FILE_CONFIG_FOR_TEST

    @classmethod
    def get_input_csv_file_path(cls, request) -> Path:
        """This method build file path if file name is presented by parametrize."""
        suffix = getattr(request, 'param', None)
        if suffix is None:
            suffix = ''
        else:
            suffix = f'_{suffix}'
        file_name = f'{request.function.__name__}{suffix}.csv'
        return cls.create_path_to_resource_directory(request.function) / file_name
