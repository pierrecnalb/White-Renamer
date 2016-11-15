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
import os.path
import shutil
import abc
import uuid


class FileSystemTreeNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, unique_id, path, parent=None):
        """
        Args:
             name = a FolderName or a FileName
        """
        self._unique_id = unique_id
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        self._set_path(path)
        self._backup_path = path
        self._size = os.path.getsize(path)  # return 0 when folders.
        self._modified_date = os.path.getmtime(path)
        self._created_date = os.path.getctime(path)
        self._is_filtered = False

    def __repr__(self):
        """override string representation of the class"""
        return self._original_basename

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def path(self):
        return self._path

    def _set_basename(self, path):
        (_, basename) = os.path.split(self._path)
        self._original_basenme = basename
        self._modified_basename = ""
        self._is_hidden = basename.startswith('.')

    def _set_path(self, path):
        """Sets the path. This will reset the changes made to the name."""
        self._path = path
        self._set_basename(path)

    @property
    def original_basename(self):
        return self._original_basename

    @property
    def modified_basename(self):
        return self._modified_basename

    @modified_basename.setter
    def modified_basename(self, value):
        self._modified_basename = value

    @property
    def parent(self):
        return self._parent

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
    def is_filtered(self):
        return self._is_filtered

    @is_filtered.setter
    def is_filtered(self, value):
        self._is_filtered = value

    def _get_modified_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset if renamed."""
        return os.path.join(self.parent.path, self.modified_basename)

    def _move(self, original_path, modified_path):
        try:
            # verify if the chosen parameters do not lead to naming conflicts.
            if self.parent.has_conflicting_children_name():
                raise Exception("Naming conflict error. Several items in the same folder have the same name. This may cause data loss. Please choose new options to avoid duplicates.")
            new_path = self.modified_path
            # find if new name is already taken by another file.
            if os.path.exists(self.modified_path):
                # get tree node with the same name.
                conflicting_tree_node = self.parent.find_child_by_path(new_path)
                # verify if the conflicting tree node is not in fact the same tree node. (i.e. no changes)
                if conflicting_tree_node is not None:
                    if self.unique_id != conflicting_tree_node.unique_id:
                        # rename conflicting tree node with a unique temporary name.
                        conflicting_name_backup = conflicting_tree_node.modified_name
                        conflicting_tree_node.modified_name = str(uuid.uuid4())
                        conflicting_tree_node.rename()
                        # get the conflicting tree node back to its original settings.
                        conflicting_tree_node.modified_name = conflicting_name_backup
            # rename current node.
            shutil.move(original_path, modified_path)
            # apply new path to the tree nodes, so that child nodes will stil have a valid path.
            self.path = self._get_modified_path
        except IOError as e:
            raise Exception(str(e))

    def rename(self):
        self._move(self.path, self._get_modified_path)

    def reset(self):
        self._move(self.path, self._backup_path)
