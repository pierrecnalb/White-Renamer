#!/usr/bin/python3

import os
from enum import Enum
from .node import Node


class File(Node):
    def __init__(self, unique_id, path, parent_node=None):
        """ Describes a file in the filesystem.

        Args:
            unique_id (int): An integer representing the id of the node.
            path (string): The full path of the node.
            parent (Node, optional): The directory node containing this node.
        """
        super().__init__(unique_id, path, parent_node)
        self._set_file_type()

    @property
    def file_type(self):
        return self._file_type

    @property
    def extension(self):
        return self._extension

    @property
    def new_extension(self):
        return self._new_extension

    @new_extension.setter
    def new_extension(self, value):
        self._new_extension = value

    def _get_new_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset if renamed."""
        return super()._get_new_path() + "." + self.new_extension

    @property
    def path(self):
        """ The full path of this file (extension included).."""
        return super().path + "." + self._extension

    def _set_path(self, path):
        (pathname, extension) = os.path.splitext(path)
        super()._set_path(pathname)  # Change path and basename.
        self._extension = extension[1:]  # remove dot
        self._new_extension = ""

    def _set_file_type(self):
        music_extensions = [
            '.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4'
        ]
        image_extensions = [
            '.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp', '.eps', '.im',
            '.jfif', '.j2p', '.jpx', '.pcx', '.ico', '.icns', '.psd', '.nef',
            'cr2', 'pef'
        ]
        if (self._extension in music_extensions):
            self._file_type = Types.music
        if (self._extension in image_extensions):
            self._file_type = Types.image
        else:
            self._file_type = Types.normal

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.folders_only:
            return True
        if file_filter.file_type is not self._file_type:
            return True
        return False


class Types(Enum):
    document = 1
    music = 2
    image = 4
    video = 8
    other = 16
    all = 31


class NodeType(Enum):
    all = 0
    folder = 1,
    file = 2


