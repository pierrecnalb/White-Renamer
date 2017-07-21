#!/usr/bin/python3

import os.path
import abc
import re
from enum import Enum
from .path import FileSystemPath


class FileSystemNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, path, parent, model):
        """ An abstract filesystem node (Base class for a file or a directory.)

        Args:
            path (string): The full path of the node.
            parent (Node): The directory node containing this node.

            model (FileSystemModel): The FileSystemModel in which this node belongs to.
        """
        self._model = model
        self._id = self._model._new_id()
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        self._backup_path = path
        self._original_path = FileSystemPath(path, parent, model)
        self._modified_path = FileSystemPath(path, parent, model)
        self._modified_path.basename = ""
        self._size = os.path.getsize(path)  # return 0 when folders.
        self._modified_date = os.path.getmtime(path)
        self._created_date = os.path.getctime(path)

    def __repr__(self):
        """Override string representation of the class."""
        return self._original_path._fullname

    @property
    def id(self):
        """int: The id of the node."""
        return self._id

    @property
    def original_path(self):
        return self._original_path

    def _set_original_path(self, value):
        self._original_path = value

    @property
    def modified_path(self):
        return self._modified_path

    @property
    def parent(self):
        return self._parent

    @property
    def size(self):
        return self._size

    @property
    def modified_date(self):
        return self._modified_date

    @property
    def created_date(self):
        return self._created_date

    @property
    def is_hidden(self):
        """ Specifies whether this node is hidden or not.
        """
        return self.original_path.basename.startswith('.')

    def is_filtered(self, file_filter):
        if file_filter.discard_hidden_files is not self.is_hidden:
            return True
        if re.match(file_filter.search_pattern, self._basename):
            return True
        return False

    def remove(self):
        """Remove the current node from the filesystem model"""
        if self.parent is not None:
            self.parent.remove_child(self)
            self._model.remove(self)


class FileSystemNodeType(Enum):
    folder = 1
    file = 2
