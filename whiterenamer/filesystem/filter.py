#!/usr/bin/python3

from .node import FileSystemNodeType
from .file import FileTypes


class Filter(object):
    def __init__(self):
        """ A filter that allows a filesystem model
        to discard specific files based on its properties.
        """
        self._discard_hidden_files = True
        self._node_type = FileSystemNodeType.file
        self._file_type = FileTypes.all
        self._search_pattern = ""

    @property
    def discard_hidden_files(self):
        """ Specifies whether the hidden files must be used or not."""
        return self._discard_hidden_files

    @discard_hidden_files.setter
    def discard_hidden_files(self, value):
        self._discard_hidden_files = value

    @property
    def node_type(self):
        return self._node_type

    @node_type.setter
    def node_type(self, value):
        self._node_type = value

    @property
    def file_type(self):
        self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value

    @property
    def search_pattern(self):
        """ The pattern used to search only specific file nodes."""
        self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        """ Specify a pattern used to select only specific file nodes."""
        self._search_pattern = value
