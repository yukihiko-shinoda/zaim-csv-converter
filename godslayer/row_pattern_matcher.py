"""This module implements row pattern matcher."""
import re


class RowPatternMatcher:
    """This class implements row pattern matcher."""
    @staticmethod
    def is_matched(list_pattern, row) -> bool:
        """Returns whether all column is same or match with pattern or not."""
        for column, pattern in zip(row, list_pattern):
            compiled_pattern = re.compile(pattern, re.UNICODE)
            if column != pattern and not compiled_pattern.search(column):
                return False
        return True
