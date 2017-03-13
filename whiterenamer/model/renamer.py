#!/usr/bin/python3

from file_system_tree_model import FileSystemTreeModel
from file_system_action import FileSystemAction
import action_descriptor


class Renamer(object):

    def __init__(self, root_path, is_recursive=False, file_filter=None):
        self._file_system_tree_model = FileSystemTreeModel(root_path, is_recursive)
        self._ordered_action_list = list()

    @property
    def file_filter(self):
        return self._file_systme_tree_model.file_filter

    @property
    def is_recursive(self):
        return self._file_system_tree_model.is_recursive

    @is_recursive.setter
    def is_recursive(self, value):
        self._file_system_tree_mode.is_recursive = value

    def append_action(self, action_name, *parameters, apply_on_extension=False):
        file_system_action = self._create_action(action_name, *parameters)
        self._ordered_action_list.append(file_system_action)
        return file_system_action

    def remove_action_at(self, index):
        self._ordered_action_list.pop(index)

    def remove_action(self, file_system_action):
        self._ordered_action_list.remove(file_system_action)

    def invoke_actions(self):
        for node in self._file_system_tree_model.filtered_nodes:
            for file_system_action in self._ordered_action_list:
                if file_system_action.apply_on_extension:
                    node.modified_extension += file_system_action.modify(node.original_extension)
                else:
                    node.modified_basename += file_system_action.modify(node.original_basename)

    # def preview(self):
    #     modified_names = list()
    #     for tree_node in self._file_system_tree_model.all_nodes:
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

    def _create_action(self, action_name, *parameters, apply_on_extension=False):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return FileSystemAction(action_instance, apply_on_extension)
