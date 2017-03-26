#!/usr/bin/python3


class StringSlicer(object):
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
        self._first_portion = ""
        self._sliced_portion = ""
        self._last_portion = ""
        if start is None:
            self._first_portion = self._string
        else:
            if end is None:
                self._first_portion = self._string[:start]
                self._sliced_portion = self._string[start:]
            else:
                self._first_portion = self._string[:start]
                self._sliced_portion = self._string[start:end]
                self._last_portion = self._string[end:]

    @property
    def string(self):
        return self._string

    @property
    def first_portion(self):
        return self._first_portion

    @property
    def sliced_portion(self):
        return self._sliced_portion

    @property
    def last_portion(self):
        return self._last_portion
