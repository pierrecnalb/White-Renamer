#!/usr/bin/python3

from file_type import FileType


class FileFilter(object):
    """
    Contains all the FileSystemTreeNodes representing the files system structure with or without the subdirectories, starting from the input path.
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
        if(value is True):
            self._folders_only = False
        self._files_only = value

    @property
    def folders_only(self):
        return self._folders_only

    @folders_only.setter
    def folders_only(self, value):
        if(self._files_only is True):
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
