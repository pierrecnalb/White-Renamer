#!/usr/bin/python3
import os


class Path(object):
    def __init__(self, parent_node, name):
        self._parent_node = parent_node
        self._fullname = name
        self._is_directory = os.path.isdir(self._path)
        if self._is_directory:
            self._extension = ""
        else:
            (_, self._extension) = os.path.splitext(parent_node.path)

    def __repr__(self):
        return self._path

    def _path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset
        if renamed.
        """
        # root node
        if(self.parent_node is None):
            return os.path.join(self.parent_node.model._path_to_root, self._fullname)
        else:
            return os.path.join(self.parent_node.path, self._fullname)

    @property
    def basename(self):
        return self._basename

    @basename.setter
    def basename(self, value):
        self._basename = value

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, value):
        self._extension = value

    @property
    def fullname(self):
        if(self._is_directory):
            return self._basename
        else:
            return self._basename + "." + self._extension
