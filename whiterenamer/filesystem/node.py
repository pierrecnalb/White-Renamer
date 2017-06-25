#!/usr/bin/python3

import os.path
import shutil
import abc
import uuid
import re
from enum import Enum
from name import Name


class FileSystemNode(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, path, parent, model):
        """ An abstract filesystem node (Base class for a file or a directory.)

        Args:
            path (string): The full path of the node.
            parent (Node): The directory node containing this node.

            model (FileSystemModel): The FileSystemModel in which this node belongs to.
        """
        self._model = model
        self._id = self._model._new_id()
        self._parent = parent
        if parent is not None:
            parent.add_child(self)
        self._backup_path = path
        self._original_name = Name(path)
        self._modified_name = Name(path)
        self._size = os.path.getsize(path)  # return 0 when folders.
        self._modified_date = os.path.getmtime(path)
        self._created_date = os.path.getctime(path)
        self._is_filtered = False

    def __repr__(self):
        """Override string representation of the class."""
        return self._original_name.fullname

    @property
    def id(self):
        """int: The id of the node."""
        return self._id

    @property
    def original_name(self):
        self._original_name

    @property
    def modified_name(self):
        self._modified_name

    @property
    def directory_path(self):
        """Since a parent folder may have been renamed during the renaming process,
        the original path to the current node may not be correct anymore.
        We need to get back to the parent path that should have been reset
        if renamed.
        """
        node_name_stack = []
        node = self
        while node.parent is not None:
            node = node.parent
            node_name_stack.insert(0, node.name.fullname)
        (path_before_root, _) = os.path.split(node._path)
        return os.path.join(path_before_root, *node_name_stack)

    @property
    def original_path(self):
        return os.path.join(self.directory_path, self.original_name.fullname)

    @property
    def modified_path(self):
        return os.path.join(self.directory_path, self.modified_name.fullname)

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
        return self.name.basename.startswith('.')

    @property
    def is_folder(self):
        return self._is_folder

    def is_filtered(self, file_filter):
        if file_filter.discard_hidden_files is not self._is_hidden:
            return True
        if re.match(file_filter.search_pattern, self._basename):
            return True
        return False




            // TODO: il faut vérifier si le noeud qui a le même nom va être renommer plus tard.
            // Si oui, suivre la même philosophie.
            // Si non, lever une exception.
    def _move(self, original_path, modified_path):
        if(original_path is modified_path):
            return
        try:
            # verify if the chosen parameters do not lead to naming conflicts.
            self._check_children_name_conflict()
            # find if new name is already taken by another file.
            if os.path.exists(modified_path):
                # Verify if a node has 
                conflicting_node = self.parent.find_child_by_path(modified_path)
                if conflicting_node is not None:
                    if self.unique_id != conflicting_node.unique_id:
                        # rename conflicting tree node
                        # with a unique temporary name.
                        conflicting_name_backup = conflicting_node.new_name
                        conflicting_node.modified_name = str(uuid.uuid4())
                        conflicting_node.rename()
                        # get the conflicting tree node back to its original settings.
                        conflicting_node.modified_name = conflicting_name_backup
            # rename current node.
            shutil.move(original_path, modified_path)
            # apply new path to the tree nodes, so that child nodes will stil have a valid path.
            self._original_path = self._set_path(new_path)
        except IOError as e:
            raise Exception(str(e))

    def rename(self):
        if(self.original_path is self.modified_path):
            return
        try:
            shutil.move(original_path, modified_path)
        except IOError as e:
            raise Exception(str(e))

    def reset(self):
        path = os.path.join(self.directory_path, self.original_name.fullname)
        self._move(path, self._backup_path)


class FileSystemNodeType(Enum):
    folder = 1
    file = 2
