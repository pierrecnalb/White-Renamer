#!/usr/bin/python3

from file_system_tree_node import FilesystemNode


class FolderNode(FilesystemNode):
    def __init__(self, unique_id, path, parent_node=None):
        """
        A directory in the file system tree node.
        Parameters:
            --path: the full path of the folder.
        """
        super().__init__(unique_id, path, parent_node)
        self._children = []

    @property
    def has_children(self):
        return self._children.length > 0

    def add_child(self, file_system_tree_node):
        self._children.append(file_system_tree_node)
        return file_system_tree_node

    @property
    def children(self):
        return self._children

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.files_only:
            return True
        return False

    def has_conflicting_children_name(self):
        """Finds if there are duplicate files/folders.
        If there are some duplicates, appends a counter to differenciate them."""
        unique_names = []
        for child_node in self.children:
            if (child_node.modified_basename not in unique_names):
                unique_names.append(child_node.modified_basename)
            else:
                return True
        return False

    def find_child_by_path(self, path):
        for child in self.children:
            if child.original_path in path:
                return child
