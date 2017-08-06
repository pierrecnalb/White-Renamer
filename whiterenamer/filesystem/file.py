#!/usr/bin/python3

from ..enummask import EnumMask
from .node import FileSystemNode


class File(FileSystemNode):
    music_extensions = ['.flac', '.mp3', '.m4a', '.ogg', '.wma', '.m3a', '.mp4']
    image_extensions = [
        '.jpg', '.jpeg', '.tif', '.png', '.gif', '.bmp', '.eps', '.im', '.jfif', '.j2p', '.jpx',
        '.pcx', '.ico', '.icns', '.psd', '.nef', 'cr2', 'pef'
    ]

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
        extension = self.original_path.extension
        if (extension in File.music_extensions):
            self._file_type = FileTypes.music
        if (extension in File.image_extensions):
            self._file_type = FileTypes.image
        else:
            self._file_type = FileTypes.document

    def is_filtered(self, file_filter):
        # if not super().is_filtered(file_filter):
        #     return False
        # if file_filter.node_type is FileSystemNodeType.folder:
        #     return False
        # if file_filter.file_type is not self._file_type:
        #     return False
        return True


class FileTypes(EnumMask):
    document = 0
    music = 1
    image = 2
    video = 4
    other = 8
    all = document | music | image | video | other
