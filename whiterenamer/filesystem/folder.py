#!/usr/bin/python3

from .node import Node


class Folder(Node):
    def __init__(self, unique_id, path, parent_node=None):
        """ Describes a directory in the filesystem.

        Args:
            unique_id (int): An integer representing the id of the node.
            path (string): The full path of the node.
            parent (Node, optional): The directory node containing this node.
        """
        super().__init__(unique_id, path, parent_node)
        self._children = []

    @property
    def has_children(self):
        """ Specifies whether the current folder contains any nodes."""
        return self._children.length > 0

    def add_child(self, node):
        self._children.append(node)
        return node

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
        """ Specifies whether there are naming duplicates among the direct children.
        """
        unique_names = []
        for child_node in self.children:
            if (child_node.new_name not in unique_names):
                unique_names.append(child_node.modified_basename)
            else:
                return True
        return False

    def find_child_by_path(self, path):
        for child in self.children:
            if child.original_path in path:
                return child
