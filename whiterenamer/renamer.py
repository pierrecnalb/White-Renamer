#!/usr/bin/python3

import file_system_tree_model


class Renamer(object):
    def __init__(self, root_path, is_recursive=False, file_filter=None):
        self._file_system_tree_model = FileSystemTreeModel(root_path, is_recursive)
        self._action_collection = ActionCollection()

    @property
    def file_filter(self):
        return self._file_systme_tree_model.file_filter

    @property
    def is_recursive(self):
        return self._file_system_tree_model.is_recursive

    @is_recursive.setter
    def is_recursive(self, value):
        self._file_system_tree_mode.is_recursive = value

    @property
    def action_collection(self):
        return self._file_system_action_collection

    def invoke_actions(self):
        for filesystem_node in self._file_system_tree_model.filtered_nodes:
            for action in self.action_collection:
                action.execute(filesystem_node)

    def batch_rename(self):
        for node in self._all_nodes:
            node.rename()

    def reset(self):
        """Reset the modified filedescriptor with the original one."""
        for node in self._all_nodes:
            node.reset()
