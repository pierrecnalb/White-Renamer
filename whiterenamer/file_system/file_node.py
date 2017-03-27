#!/usr/bin/python3

import os
from file_type import FileType
from file_system_tree_node import FilesystemNode


class FileNode(FilesystemNode):
    def __init__(self, unique_id, path, parent_node=None):
        super().__init__(unique_id, path, parent_node)
        self._set_file_type()

    @property
    def file_type(self):
        return self._file_type

    @property
    def extension(self):
        return self._original_extension

    @extension.setter
    def extension(self, value):
        self._modified_extension = value

    def _get_modified_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset if renamed."""
        return super()._get_modified_path() + "." + self.modified_extension

    @property
    def path(self):
        return super().path + "." + self._original_extension

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

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.folders_only:
            return True
        if file_filter.file_type is not self._file_type:
            return True
        return False
