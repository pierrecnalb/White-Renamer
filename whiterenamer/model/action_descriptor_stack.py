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


class ActionDescriptorStack(object):

    def __init__(self):
        self._action_stack = list()

    def append_action(self, action_descriptor):
        self._action_stack.append(action_descriptor)

    def insert_action(self, index, action_descriptor):
        self._action_stack.insert(index, action_descriptor)

    def remove_action(self, action_descriptor):
        self._action_stack.remove(action_descriptor)

    def execute_all_actions(self, model):
        for action in self._action_stack:
            action.invoke_action(model)

    def rename_all(self, tree_node_model):
        for tree_node in tree_node_model.root_node.children:
            print(tree_node.original_basename)
            print(tree_node.modified_basename)
            tree_node.rename()
