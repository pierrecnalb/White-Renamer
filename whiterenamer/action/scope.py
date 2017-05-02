#!/usr/bin/python3

from enum import Enum


class Targets(Enum):
    """Specifies the filesystem node scope."""
    foldername = 1
    filename = 2
    extension = 4


class StringRange(object):
    def __init__(self, start=0, end=None):
        """
        Defines a range.

        Args:
            start: The starting index of the range.
                0 being the beginning of the string, None being the end of the string.
                Negative numbers can be used to start the count from the end.
            end: The ending index of the range.
                0 being the beginning of the string, None being the end of the string.
                Negative numbers can be used to start the count from the end.
        """

        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class Tokenizer(object):
    def __init__(self, string, string_range):
        """
        Slices the given string into several tokens.

        Args:
            string (string): The string to tokenize.
            string_range (StringRange): The range used to define the portion of the string that should be tokenized.
        """
        self._string = string
        start = string_range.start
        end = string_range.end
        self._first_token = ""
        self._selected_token = ""
        self._last_token = ""
        if start is None:
            self._first_token = self._string
        else:
            if end is None:
                self._first_token = self._string[:start]
                self._selected_token = self._string[start:]
            else:
                self._first_token = self._string[:start]
                self._selected_token = self._string[start:end]
                self._last_token = self._string[end:]

    @property
    def string(self):
        return self._string

    @property
    def first_token(self):
        return self._first_token

    @property
    def selected_token(self):
        return self._selected_token

    @property
    def last_token(self):
        return self._last_portion
