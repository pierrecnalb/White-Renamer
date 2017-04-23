#!/usr/bin/python3


class StringRange(object):
    def __init__(self, start=0, end=None):
        """
        Defines a range.
        args:
        start: The starting point of the range. 0 being the first index, None the last index.
        end: The ending point of the range. 0 being the first index, None the last index.
        (Negative numbers can be used to start the count from the last index.)
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
        Extracts a portion of the given name.
        args:
        start: The starting point of the range. 0 being the first letter of the name.
        end: The ending point of the range. 0 being the last letter of the name.
        (Negative numbers can be used to start the count from the last index.)
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
