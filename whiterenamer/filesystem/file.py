#!/usr/bin/python3

import os
from .node import FileSystemNode
from ..enummask import EnumMask


class File(FileSystemNode):
    def __init__(self, path, parent_node, model):
        """ Describes a file in the filesystem.

        Args:
            path (string): The full path of the node.
            parent (FileSystemNode, optional): The directory node containing this node.
            model (FileSystemModel): The FileSystemModel in which this node belongs to.
        """
        super().__init__(path, parent_node, model)
        self._set_file_type()

    @property
    def file_type(self):
        return self._file_type

    def _set_file_type(self):
        music_extensions = ['.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4']
        image_extensions = [
            '.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp', '.eps', '.im', '.jfif', '.j2p', '.jpx',
            '.pcx', '.ico', '.icns', '.psd', '.nef', 'cr2', 'pef'
        ]
        if (self.name.extension in music_extensions):
            self._file_type = FileTypes.music
        if (self.name.extension in image_extensions):
            self._file_type = FileTypes.image
        else:
            self._file_type = FileTypes.document

    def is_filtered(self, file_filter):
        if super().is_filtered(file_filter):
            return True
        if file_filter.folders_only:
            return True
        if file_filter.file_type is not self._file_type:
            return True
        return False


class FileTypes(EnumMask):
    document = 0
    music = 1
    image = 2
    video = 4
    other = 8
    all = document | music | image | video | other
