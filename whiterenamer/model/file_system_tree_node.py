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
import copy


class FileSystemTreeNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, unique_id, name, parent_node=None):
        """
        Args:
             name = a FolderName or a FileName
        """
        self._unique_id = unique_id
        self._parent_node = parent_node
        if parent_node is not None:
            parent_node.add_child(self)
        self._original_name = name
        self._backup_name = name
        self._modified_name = name
        self._size = os.path.getsize(self.full_path)  #return 0 when folders.
        self._modified_date = os.path.getmtime(self.full_path)
        self._created_date = os.path.getctime(self.full_path)
        self._is_hidden = name.startswith('.')
        self._is_filtered = False

    def __repr__(self):
        """override string representation of the class"""
        return self._original_name

    @property
    def unique_id(self):
        return self._unique_id

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

    @property
    def parent(self):
        return self._parent_node

    @abc.abstractmethod
    def parent_path(self):
        """"""
        return

    @abc.abstractmethod
    def basename(self):
        """"""
        return

    @property
    def original_path(self):
        return os.path.join(self.parent_path, self.original_name)

    @property
    def modified_path(self):
        return os.path.join(self.parent_path, self.modified_name)

    @property
    def backup_path(self):
        return os.path.join(self.parent_path, self.backup_name)

    # def relative_path_to_root(self):
    #     if self._parent != None:
    #         return os.path.join(self.parent.relative_path_to_root,
    #                             self.name)
    #     else:
    #         return self.name


    @property
    def full_path(self):
        return os.path.join(self.parent_path, self.original_name)
        # return os.path.join(self._root_path, self.get_relative_path())

    def rename(self):
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
            shutil.move(self.original_path, self.modified_path)
            # apply new names to the tree nodes.
            self.original_name = copy.deepcopy(self.modified_name)
        except IOError as e:
            raise Exception(str(e))


    def reset(self):
        shutil.move(self.original_path, self.backup_path)
        self._original_name = self._backup_name
