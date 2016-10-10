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


class TreeNodeNameSlicer(object):

    def __init__(self, file_system_tree_node, name_range):
        self._file_system_tree_node = file_system_tree_node
        self._name_range = name_range
        unmodified_name = self._get_unmodified_name()
        self._sliced_name = unmodified_name[
            name_range.get_start_index(unmodified_name):
            name_range.get_end_index(unmodified_name)]

    def _get_unmodified_name(self):
        return self._file_system_tree_node.modified_name

    @property
    def sliced_name(self):
        return self._sliced_name

    def _get_unmodified_sliced_name(self, file_system_tree_node, action_range):
        """Gets the portion of the name defined by the action_range."""
        # modified_name is used, so that several actions can be piped.
        unmodified_name = self._get_unmodified_name(file_system_tree_node)
        return self._get_unmodified_name[action_range.get_start_index(unmodified_name):action_range.get_end_index(
            unmodified_name)]

    def _get_new_name(self, file_system_tree_node, action_range):
        name = file_system_tree_node.modified_name
        name[0:action_range.start] + self._get_modified_sliced_name(file_system_tree_node,
                                                                    action_range) + name[action_range.end:]
        return name

