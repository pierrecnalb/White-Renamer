#!/usr/bin/python3
import os


class FileSystemPath(object):
    def __init__(self, path, parent_node, model):
        self._parent_node = parent_node
        self._model = model
        (directory, fullname) = os.path.split(path)
        self._is_directory = os.path.isdir(path)
        self.fullname = fullname

    def __repr__(self):
        return self._path()

    @property
    def absolute(self):
        return self._path()

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
        if self._is_directory:
            return self.basename
        else:
            return self.basename + "." + self.extension

    @fullname.setter
    def fullname(self, value):
        if self._is_directory:
            self._basename = value
            self._extension = ""
        else:
            (self._basename, self._extension) = os.path.splitext(value)
            self._extension = self._extension[1:]  # Let's remove the dot.

    def _path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset
        if renamed.
        """
        # root node
        if (self._parent_node is None):
            return os.path.join(self._model._path_to_root, self.fullname)
        else:
            return os.path.join(self._parent_node.original_path.absolute, self.fullname)
