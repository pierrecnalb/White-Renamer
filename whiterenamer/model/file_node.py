#!/usr/bin/python3

import os
from file_type import FileType
from file_system_tree_node import FileSystemTreeNode


class FileNode(FileSystemTreeNode):
    def __init__(self, unique_id, path, parent_node=None):
        super().__init__(unique_id, path, parent_node)
        self._set_file_type()

    @property
    def file_type(self):
        return self._file_type

    @property
    def original_extension(self):
        return self._original_extension

    @property
    def modified_extension(self):
        if self._modified_extension is None:
            return self.original_extension
        return self._modified_extension

    @modified_extension.setter
    def modified_extension(self, value):
        self._modified_extension = value

    def _get_modified_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset if renamed."""
        return super()._get_modified_path() + "." + self.modified_extension

    @property
    def path(self):
        return super().path + "." + self.original_extension

    def _set_path(self, path):
        (pathname, extension) = os.path.splitext(path)
        super()._set_path(pathname)  # Change path and basename.
        self._original_extension = extension[1:]  # remove dot
        self._modified_extension = None

    def _set_file_type(self):
        music_extensions = ['.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4']
        image_extensions = ['.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp',
                            '.eps', '.im', '.jfif', '.j2p', '.jpx', '.pcx',
                            '.ico', '.icns', '.psd', '.nef', 'cr2', 'pef']
        if (self._original_extension in music_extensions):
            self._file_type = FileType.music
        if (self._original_extension in image_extensions):
            self._file_type = FileType.image
        else:
            self._file_type = FileType.normal

    # def match_files_type(self, files_type):
    #     if (files_type == ['*.*']):
    #         return True
    #     if (files_type == ["folders"]):
    #         if (self.is_folder is True):
    #             return True
    #         else:
    #             return False
    #     elif (self.is_folder is False):
    #         name = self.original_filedescriptor.extension.lower()
    #         for ext in files_type:
    #             if (name in ext):
    #                 return True
    #     return False

    # def match_name_filter(self, name_filter):
    #     if (name_filter == ""):
    #         return True
    #     if (self.is_folder is False):
    #         name = str(self.original_filedescriptor.filename).lower()
    #     else:
    #         name = str(self.original_filedescriptor.foldername).lower()
    #     if (name_filter in name):
    #         return True
    #     return False
