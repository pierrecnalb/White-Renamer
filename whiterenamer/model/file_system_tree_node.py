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
import copy
import abc


class FileSystemTreeNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, unique_id, name_composer, parent_node):
        """
        Args:
             name = a FolderName or a FileName
        """
        self._unique_id = unique_id
        self._parent_node = parent_node
        self._original_name = name_composer.full_name
        self._backup_name = self._original_name
        self._modified_name = name_composer
        self._size = getsize(self._full_path)  #return 0 when folders.
        self._modified_date = getmtime(self._full_path)
        self._created_date = getctime(self._full_path)
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

    @property
    def modified_name(self):
        return self._modified_name

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


    # def full_path(self):
    #     return join(self._root_path, self.get_relative_path())


    def rename(self):
        try:
            #verify if the chosen parameters do not lead to naming conflicts.
            if self.parent.has_conflicting_children_name():
                raise Exception("Naming conflict error. Several items in the same folder have the same name. This may cause data loss. Please choose new options to avoid duplicates.")
            new_path = tree_node.modified_path
            #find if new name is already taken by another file.
            if os.path.exists(self.modified_path):
                #get tree node with the same name.
                conflicting_tree_node = tree_node.parent.find_child_by_path(new_path)
                #verify if the conflicting tree node is not in fact the same tree node. (i.e. no changes)
                if conflicting_tree_node is not None:
                    if tree_node.unique_id != conflicting_tree_node.unique_id:
                        #rename conflicting tree node with a unique temporary name.
                        conflicting_name_backup = conflicting_tree_node.modified_name
                        conflicting_tree_node.modified_name = str(uuid4())
                        conflicting_tree_node.rename()
                        #get the conflicting tree node back to its original settings.
                        conflicting_tree_node.modified_name = conflicting_name_backup
            #rename current node.
            shutil.move(tree_node.original_path, tree_node.modified_path)
            #apply new names to the tree nodes.
            tree_node.original_name = deepcopy(tree_node.modified_name)
        except IOError as e:
            raise Exception(str(e))


    def reset(self):
        shutil.move(self.original_path, self.backup_path)
        self._original_name = self._backup_name
