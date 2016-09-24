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
import os
import FileSystemTreeNode
import FileName


class FileNode(FileSystemTreeNode):

    def __init__(self, path, file_type = FileType.normal):
        (parent_path, basename) = os.path.split(path)
        (name, extension) = os.path.splitext(basename)
        # remove dot
        self._extension = extension[1:]

        self._name = Name.__init__(name)
        self._file_type = file_type
        FileSystemTreeNode.__init__(parent_path, self._name)
        self._set_file_type()


    def name(self):
        """Gets the full name of the file."""
        return FileSystemTreeNode.name + "." + self._extension

    @property
    def file_type(self):
        return self._file_type

    def _set_file_type(self):
        music_extensions = ['.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4']
        image_extensions = ['.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp', '.eps', '.im', '.jfif', '.j2p', '.jpx', '.pcx', '.ico', '.icns', '.psd', '.nef', 'cr2', 'pef']
        if(self._extension in music_extension):
            self._file_type = FileType.music
        if(self._extension in image_extension):
            self._file_type = FileType.image
        else:
            self._file_type = FileType.normal


    def match_files_type(self, files_type):
        if (files_type == ['*.*']):
            return True
        if (files_type == ["folders"]):
            if (self.is_folder is True):
                return True
            else:
                return False
        elif (self.is_folder is False):
            name = self.original_filedescriptor.extension.lower()
            for ext in files_type:
                if (name in ext):
                    return True
        return False

    def match_name_filter(self, name_filter):
        if (name_filter == ""):
            return True
        if (self.is_folder is False):
            name = str(self.original_filedescriptor.filename).lower()
        else:
            name = str(self.original_filedescriptor.foldername).lower()
        if (name_filter in name):
            return True
        return False
