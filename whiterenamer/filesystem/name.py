#!/usr/bin/python3
import os


class Name(object):
    def __init__(self, path):
        (self._directory_path, self._basename) = os.path.split(path)
        self._is_directory = os.path.isdir(path)
        if self._is_directory:
            self._extension = ""
        else:
            (_, self._extension) = os.path.splitext(path)

    def __repr__(self):
        return self.fullname

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
