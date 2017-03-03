#!/usr/bin/python3

from file_system_tree_model import FileSystemTreeModel
import action_descriptor


class Renamer(object):

    def __init__(self, root_path, is_recursive):
        self._file_system_tree_model = FileSystemTreeModel(root_path, is_recursive)
        self._action_stack = list()
        self._all_nodes = self._file_system_tree_model.list_all_nodes()

    def _create_action(self, action_name, *parameters):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return action_instance

    def append_action(self, action_name, *parameters):
        action_instance = self.create_action(action_name, *parameters)
        self._action_stack.append(action_instance)

    def add_extension_action(self, action):
        self._action_stack.append(action)

    def invoke_actions(self):
        for action in self._action_stack:
            for node in self._all_nodes:
                node.modified_basename += action.modify(node.original_basename)

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
