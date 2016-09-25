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


class NameComposer(object):
    """Describes a name based on a prefix, a basename and a suffix."""

    def __init__(self, basename):
        self._full_name = basename
        self._basename = basename
        self._prefix = ""
        self._suffix = ""

    def __repr__(self):
        """override string representation of the class"""
        return self.full_name

    @property
    def basename(self):
        return self._basename

    @basename.setter
    def basename(self, value):
        self._basename = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        self._suffix = value

    @property
    def full_name(self):
        """Gets the full name."""
        self._full_name = self._prefix + self._basename + self._suffix
