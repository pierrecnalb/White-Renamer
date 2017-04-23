#!/usr/bin/python3

import os
from enum import Enum
from node import Node


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
            self._file_type = FileType.music
        if (self._extension in image_extensions):
            self._file_type = FileType.image
        else:
            self._file_type = FileType.normal

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.folders_only:
            return True
        if file_filter.file_type is not self._file_type:
            return True
        return False


class FileType(Enum):
    normal = 0
    music = 1
    image = 2
    video = 3


class FileFilter(object):
    """
    Contains all the FilesystemNodes representing the files system structure with or without the subdirectories, starting from the input path.
    Parameters:
        --input_path: string that represents the root directory to start the files collection from.
        --use_subdirectory: boolean that tells to look over the subdirectories recursively or not.
    """

    def __init__(self):
        # self._is_recursive = False
        self._show_hidden_files = False
        self._files_only = False
        self._folders_only = False
        self._files_type = FileType.all
        self._search_pattern = ""

    @property
    def show_hidden_files(self):
        return self._show_hidden_files

    @show_hidden_files.setter
    def show_hidden_files(self, value):
        self._show_hidden_files = value

    # @property
    # def is_recursive(self):
    #     return self._is_recursive

    # @is_recursive.setter
    # def is_recursive(self, value):
    #     self._is_recursive = value

    @property
    def files_only(self):
        return self._files_only

    @files_only.setter
    def files_only(self, value):
        if (value is True):
            self._folders_only = False
        self._files_only = value

    @property
    def folders_only(self):
        return self._folders_only

    @folders_only.setter
    def folders_only(self, value):
        if (self._files_only is True):
            self._files_only = False
        self._folders_only = value

    @property
    def files_type(self):
        self._file_type

    @files_type.setter
    def files_type(self, value):
        self._file_type = value

    @property
    def search_pattern(self):
        self._search_pattern

    @search_pattern.setter
    def search_pattern(self, value):
        self._search_pattern = value
