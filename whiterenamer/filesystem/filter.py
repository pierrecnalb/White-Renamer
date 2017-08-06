#!/usr/bin/python3

from ..event import Event
from .file import FileTypes
from .node import NodeType


class Filter(object):
    def __init__(self):
        """ A filter that allows a filesystem model
        to discard specific files based on its properties.
        """
        self._discard_hidden_files = True
        self._node_type = NodeType.file
        self._file_type = FileTypes.all
        self._search_pattern = ""
        self.changed = Event()

    def _on_changed(self):
        self.changed(None)

    @property
    def discard_hidden_files(self):
        """ Specifies whether the hidden files must be used or not."""
        return self._discard_hidden_files

    @discard_hidden_files.setter
    def discard_hidden_files(self, value):
        self._discard_hidden_files = value
        self._on_changed()

    @property
    def node_type(self):
        return self._node_type

    @node_type.setter
    def node_type(self, value):
        self._node_type = value
        self._on_changed()

    @property
    def file_type(self):
        self._file_type

    @file_type.setter
    def file_type(self, value):
        self._file_type = value
        self._on_changed()

    @property
    def search_pattern(self):
        """ The pattern used to search only specific file nodes."""
        self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        """ Specify a pattern used to select only specific file nodes."""
        self._search_pattern = value
        self._on_changed()