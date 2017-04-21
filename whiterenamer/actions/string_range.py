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
