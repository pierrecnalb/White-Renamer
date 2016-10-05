#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.


#!/usr/bin/python

class Range(object):

    class SpecialIndices(object):
        @staticmethod
        def begin(string):
            return len(string)

    BEGIN = 0
    END = SpecialIndices.begin

    def __init__(self, start, end=None):
        # Make sure start and end can be used as callables in the rest of this
        # class.
        self.start = start if callable(start) else lambda string: start
        if end is None:
                end = start
        self.end = end if callable(end) else lambda string: end

    def getStartIndex(self, string):
        return self.start(string)

    def getEndIndex(self, string):
        return self.end(string)
    
    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value

    @property
    def end(self):
        return self._start

    @end.setter
    def end(self, value):
        self._end = value

def test():
    ranges = {}
    ranges['pushFrontRange'] = Range(Range.BEGIN)
    ranges['pushBackRange'] = Range(Range.END)
    ranges['insertSomewhereRange'] = Range(3)
    ranges['replaceFromSomewhereToEnd'] = Range(3, Range.END)

  
