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
import Name
import FolderNode
import Date
import os.path
import shutil


class FileSystemTreeNode(object):

    def __init__(self, parent_path, name):
        self._parent_node = FolderNode.__init__(parent_path)
        self._original_name = name
        self._modified_name = name
        self._backup_name = name
        self._size = getsize(self._full_path)  #return 0 when folders.
        self._modified_date = getmtime(self._full_path)
        self._created_date = getctime(self._full_path)
        self._is_hidden = name.startswith('.')

    def __repr__(self):
        """override string representation of the class"""
        return self._original_name

    @property
    def size(self):
        return self._size

    @property
    def modified_date(self):
        return self._modified_date

    @property
    def created_date(self):
        return self._created_date

    @property
    def is_hidden(self):
        return self._is_hidden

    @property
    def is_folder(self):
        return self._is_folder

    @property
    def parent(self):
        return self._parent_node

    def get_relative_path(self):
        if self._parent != None:
            return os.path.join(parent.get_relative_path(),
                                self.name)
        else:
            return self.name


    def get_full_path(self):
        return join(self._root_path, self.get_relative_path())

    @property
    def original_name(self):
        return self._original_name

    @original_name.setter
    def original_name(self, value):
        self._original_name = value

    @property
    def modified_name(self):
        return self._modified_name

    @modified_name.setter
    def modified_name(self, value):
        self._modified_name = value

    @property
    def backup_name(self):
        return self._backup_name

    @backup_filedescriptor.setter
    def backup_name(self, value):
        self._backup_name = value


    def _has_name_conflict(self):
        """Finds if there are duplicate files/folders. If there are some duplicates, appends a counter to differenciate them."""
        if self.parent is not None:
            for same_level_tree_node in self.parent.children:
                if (same_level_tree_node.modified_name in children_names):
                    raise Exception(
                        "Names conflict: several items have the same name. Please choose new options to avoid duplicates.")
                else:


    def rename(self):
        try:
            has_duplicate = self.has_duplicates()
            if self._has_name_conflict:
                conflicting_tree_node = tree_node.get_parent(
                ).find_child_by_path(tree_node.get_modified_path())
                if (conflicting_tree_node is not None and
                        tree_node.get_file_system_tree_node() !=
                        conflicting_tree_node):  #check if it is the same file
                    old_conflicting_file_descriptor = conflicting_tree_node.modified_filedescriptor
                    conflicting_tree_node.modified_filedescriptor = FileDescriptor(
                        str(uuid4()) + "." +
                        tree_node.original_filedescriptor.extension,
                        tree_node.is_folder)
                    self.rename(conflicting_tree_node)
                    conflicting_tree_node.modified_filedescriptor = old_conflicting_file_descriptor
            move(tree_node.get_original_path(), tree_node.get_modified_path())
            tree_node.original_filedescriptor = deepcopy(
                tree_node.modified_filedescriptor)
            # self.reset(tree_node)
        except IOError as e:
            raise Exception(str(e))


    def undo(self):
        shutil.move(tree_node.get_original_path(), tree_node.get_backup_path())
        tree_node.original_filedescriptor = tree_node.backup_filedescriptor
