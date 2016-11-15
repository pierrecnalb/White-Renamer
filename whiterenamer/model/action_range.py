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


class ActionRange(object):

    class SpecialIndices(object):
        @staticmethod
        def end(string):
            return len(string)

    START = 0
    END = SpecialIndices.end

    def __init__(self, start=START, end=END):
        # Make sure start and end can be used as callables in the rest of this
        # class.
        self._start = start if callable(start) else lambda string: start
        self._end = end if callable(end) else lambda string: end

    def get_start_index(self, string):
        return self._start(string)

    def get_end_index(self, string):
        return self._end(string)
