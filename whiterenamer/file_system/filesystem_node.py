#!/usr/bin/python3

import os.path
import shutil
import abc
import uuid
import re


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
        self._new_name = ""

    def __repr__(self):
        """override string representation of the class"""
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def path(self):
        return self._path

    def _set_path(self, path):
        """Sets the path. This will reset the changes made to the name."""
        self._path = path
        self._set_name(path)

    def _set_name(self, path):
        (_, basename) = os.path.split(self._path)
        self._name = basename
        self._new_name = ""
        self._is_hidden = basename.startswith('.')

    @property
    def name(self):
        return self._original_name

    @property
    def new_name(self):
        return self._new_name

    @new_name.setter
    def new_name(self, value):
        self._new_name = value

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

    def is_filtered(self, file_filter):
        if file_filter.show_hidden_files is not self._is_hidden:
            return True
        if re.match(file_filter.search_pattern, self._name):
            return True
        return False

    def _get_new_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset if renamed."""
        return os.path.join(self.parent.path, self.new_name)

    def _move(self, original_path, modified_path):
        try:
            # verify if the chosen parameters do not lead to naming conflicts.
            if self.parent.has_conflicting_children_name():
                raise Exception("""Naming conflict error.
                Several items in the same folder have the same name.
                This may cause data loss. Please choose new options to avoid duplicates.""")
            new_path = self._get_new_path()
            # find if new name is already taken by another file.
            if os.path.exists(new_path):
                # get tree node with the same name.
                conflicting_tree_node = self.parent.find_child_by_path(new_path)
                # verify if the conflicting tree node is not in fact the same tree node. (i.e. no changes)
                if conflicting_tree_node is not None:
                    if self.unique_id != conflicting_tree_node.unique_id:
                        # rename conflicting tree node with a unique temporary name.
                        conflicting_name_backup = conflicting_tree_node.new_name
                        conflicting_tree_node.modified_name = str(uuid.uuid4())
                        conflicting_tree_node.rename()
                        # get the conflicting tree node back to its original settings.
                        conflicting_tree_node.modified_name = conflicting_name_backup
            # rename current node.
            shutil.move(original_path, modified_path)
            # apply new path to the tree nodes, so that child nodes will stil have a valid path.
            self._path = self._set_path(new_path)
        except IOError as e:
            raise Exception(str(e))

    def rename(self):
        self._move(self.path, self._get_new_path())

    def reset(self):
        self._move(self.path, self._backup_path)