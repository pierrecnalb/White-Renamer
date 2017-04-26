#!/usr/bin/python3

import os
from enum import Enum
from .node import Node


class File(Node):
    def __init__(self, unique_id, path, parent_node=None):
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


class Filter(object):
    """
    Contains all the FilesystemNodes representing the files system structure with or without the subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
    """

    def __init__(self):
        self._show_hidden_files = False
        self._node_type = NodeType.all
        self._file_type = Types.all
        self._search_pattern = ""

    @property
    def show_hidden_files(self):
        return self._show_hidden_files

    @show_hidden_files.setter
    def show_hidden_files(self, value):
        self._show_hidden_files = value

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
        self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        self._search_pattern = value
