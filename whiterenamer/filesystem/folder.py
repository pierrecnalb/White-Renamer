#!/usr/bin/python3

from .node import FileSystemNode
from . import File


class Folder(FileSystemNode):
    def __init__(self, path, parent_node, model):
        """ Describes a directory in the filesystem.

        Args:
            path (string): The full path of the node.
            parent (FileSystemNode, optional): The directory node containing this node.
            model (FileSystemModel): The FileSystemModel in which this node belongs to.
        """
        super().__init__(path, parent_node, model)
        self._children = []

    @property
    def has_children(self):
        """ Specifies whether the current folder contains any nodes."""
        return self.children.length > 0

    def add_child(self, node):
        self._children.append(node)
        return node

    @property
    def children(self):
        """ Returns a list of the filtered children contained in this folder."""
        self._children

    def remove_child(self, node):
        """ Removes the given node from this folder."""
        self._children.remove(node)

    def get_folder_children(self):
        return filter(
            lambda child: isinstance(child, Folder), self.children)

    def get_files_children(self):
        return filter(lambda child: isinstance(child, File), self.children)

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.files_only:
            return False
        return False

    def find_child_by_path(self, path):
        for child in self.children:
            if child.original_path.absolute in path:
                return child
