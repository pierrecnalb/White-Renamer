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

import time

class Date(object):

    def __init__(time):
        self._time = time

    def __repr__(self):
        """override string representation of the class"""
        return self._name

    def format(format_keywords):
        """
        Displays the date with the specified format.
        Commonly used format_keywords are:
        %y  year with century as a decimal number.
        %m  month as a decimal number [01,12].
        %d  day of the month as a decimal number [01,31].
        %h  hour (24-hour clock) as a decimal number [00,23].
        %m  minute as a decimal number [00,59].
        %s  second as a decimal number [00,61].
        %z  time zone offset from utc.
        %a  locale's abbreviated weekday name.
        %a  locale's full weekday name.
        %b  locale's abbreviated month name.
        %b  locale's full month name.
        %c  locale's appropriate date and time representation.
        %i  hour (12-hour clock) as a decimal number [01,12].
        %p  locale's equivalent of either am or pm.
        """
        return strftime(format_keywords, localtime(self._time))
