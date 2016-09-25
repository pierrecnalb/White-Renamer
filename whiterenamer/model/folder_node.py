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
import FolderName


class FolderNode(FileSystemTreeNode):
    def __init__(self, unique_id, path, parent_node=None):
        """
        A directory in the file system tree node.
        Parameters:
            --path: the full path of the folder.
        """
        (self._parent_path, basename) = os.path.split(path)
        folder_name_composer = FolderName.__init__(basename)
        FileSystemTreeNode.__init__(unique_id, folder_name_composer,
                                    parent_node)
        self._children = []
        if parent_node is not None:
            parent_node.add_children(self)

    @property
    def has_children(self):
        return self._children.length > 0

    def add_children(self, file_system_tree_node):
        self._children.append(file_system_tree_node)
        return file_system_tree_node

    @property
    def children(self):
        return self._children

    @property
    def parent_path(self):
        return self._parent_path

    def has_conflicting_children_name(self):
        """Finds if there are duplicate files/folders. If there are some duplicates, appends a counter to differenciate them."""
        unique_names = []
        for child_node in self.children:
            if (child_node.modified_name not in unique_names):
                unique_names.append(child_node.modified_name)
            else:
                return True
        return False

    def find_child_by_path(self, path):
        for child in self.children:
            if child.original_path in path:
                return child

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
