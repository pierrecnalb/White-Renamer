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
from file_system_tree_model import FileSystemTreeModel


class Renamer(object):

    def __init__(self, root_path, is_recursive):
        self._file_system_tree_model = FileSystemTreeModel(root_path, is_recursive)
        self._action_stack = list()
        self._all_nodes = self._file_system_tree_model.list_all_nodes

    def append_action(self, action_descriptor):
        self._action_stack.append(action_descriptor)

    def add_extension_action(self, action_descriptor):
        self._action_stack.append(action_descriptor)

    def invoke_actions(self):
        for action in self._action_stack:
            action.invoke_action(self._file_system_tree_model)

    # def preview(self):
    #     modified_names = list()
    #     for tree_node in self._file_system_tree_model.list_all_nodes:
    #         tree_node.modified_name

    def batch_rename(self):
        for node in self._all_nodes:
            node.rename()

    def reset(self):
        """Reset the modified filedescriptor with the original one."""
        for node in self._all_nodes:
            node.reset()

    # def parse_renamed_files(self, input_path, sorting_criteria, reverse_order):
    #     input_path = abspath(input_path)
    #     directory_files = sorted(listdir(input_path), key = lambda file : self.get_file_sorting_criteria(join(input_path, file), sorting_criteria), reverse=reverse_order)
    #     for filename in directory_files:
    #         filepath = join(input_path, filename)
    #         if filename[0] == '.' and not self.show_hidden_files:
    #             continue
    #         if isdir(filepath):
    #             self.renamed_files_list.append(relpath(filepath,
    #                                                    self.root_folder))
    #             if (not self.use_subdirectory):
    #                 continue
    #             else:
    #                 self.parse_renamed_files(filepath, sorting_criteria,
    #                                          reverse_order)
    #         else:
    #             self.renamed_files_list.append(relpath(filepath,
    #                                                    self.root_folder))

    # def get_renamed_files(self):
    #     self.save_result_to_file("hooh", self.renamed_files_list)
