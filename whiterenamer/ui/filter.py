#!/usr/bin/python3

# Copyright (C) 2015-2016 Pierre Blanc
#
# This file is part of WhiteRenamer.
#
# WhiteRenamer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WhiteRenamer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WhiteRenamer. If not, see <http://www.gnu.org/licenses/>.

class Filter(object):
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
        self._music_files_only = False
        self._image_files_only = False


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
        if(self._folders_only is True):
            raise Exception("Files only and folders only cannot be true at the same time.")
        self._files_only = value

    @property
    def folders_only(self):
        return self._folders_only

    @folders_only.setter
    def folders_only(self, value):
        if(self._files_only is True):
            raise Exception("Files only and folders only cannot be true at the same time.")
        self._folders_only = value

    @property
    def music_files_only(self):
        return self._music_files_only

    @music_files_only.setter
    def music_files_only(self, value):
        if(self._image_files_only is True):
            raise Exception("Music files only and image files only cannot be true at the same time.")
        self._music_files_only = value

    @property
    def image_files_only(self):
        return self._image_files_only

    @image_files_only.setter
    def image_files_only(self, value):
        if(self._music_files_only is True):
            raise Exception("Music files only and image files only cannot be true at the same time.")
        self._image_files_only = value


    def all_files_type():
        self._music_files_only = False
        self._image_files_only = False

    def files_and_folders():
        self._files_only = False
        self._folders_only = False


