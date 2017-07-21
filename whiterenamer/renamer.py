#!/usr/bin/python3

import os
import shutil
import uuid
import copy
from .filesystem.model import FileSystemModel, FilteredModel
from .action.factory import ActionFactory


class Renamer(object):
    def __init__(self, root_path, is_recursive, file_filter):
        self._original_model = FileSystemModel(root_path, is_recursive)
        self._filtered_model = FilteredModel(self._original_model, file_filter)
        self._action_collection = ActionCollection()

    @property
    def filesystem_model(self):
        return self._filtered_model

    def update_model(self, file_filter):
        self._filtered_model = FileSystemModel(self._original_model, file_filter)

    @property
    def action_collection(self):
        return self._action_collection

    def invoke_actions(self):
        for filesystem_node in self._filtered_model.nodes:
            for action in self.action_collection.items:
                action.execute(filesystem_node)

    def batch_rename(self):
        ModelValidator.verify_files_integrity(self._filtered_model)
        for filesystem_node in self._filtered_model.nodes:
            self._rename(filesystem_node)

    def reset(self):
        """Reset the modified filedescriptor with the original one."""
        for node in self._all_nodes:
            node.reset()

    def _rename(self, node):
        print("rename node={0} INTO {1}".format(node.original_path.basename, node.modified_path.basename))
        if node.modified_path.basename == "" or node.modified_path.absolute == node.original_path.absolute:
            return
        try:
            # find if new name is already taken by another file.
            if os.path.exists(node.modified_path.absolute):
                conflicting_node = self._filtered_model.find_node_by_path(node.modified_path.absolute)
                if conflicting_node is None:
                    # Conflicting node is not part of the model.
                    raise Exception("TODO: write here exception")
                    # Ignore it.
                    return
                else:
                    # Check whether the conflicting node was intended to be renamed
                    if conflicting_node.modified_path.absolute == conflicting_node.original_path.absolute:
                        if self.unique_id != conflicting_node.unique_id:
                            conflicting_name_backup = conflicting_node.modified_path._fullname
                            conflicting_node.modified_path._fullname = str(uuid.uuid4())
                            self._rename(conflicting_node)
                            # get the conflicting tree node back to its original settings.
                            conflicting_node.modified_name._fullname = conflicting_name_backup
            # rename current node.
            print("RENAME***")
            shutil.move(node.original_path.absolute, node.modified_path.absolute)
            # apply new path to the node, so that child nodes will stil have a valid path.
            node._set_original_path = copy.deepcopy(node.modified_path)
        except IOError as e:
            raise Exception(str(e))


class ModelValidator(object):

    @classmethod
    def verify_files_integrity(self, filesystem_model):
        """ Performs various tests to be sure that the renaming operations are safe."""
        unique_names = set()
        for node in filesystem_model.nodes:
            self._check_user_input_duplicates(node, unique_names)
            self._check_existing_node(node, filesystem_model)

    def _is_modified_node(self, node):
        return node.modified_path.basename == "" or node.modified_path.absolute == node.original_path.absolute

    def _check_user_input_duplicates(self, node, unique_names):
        """ Check whether the user inputs does not lead to files with same names.
        """
        if (node.modified_path.absolute not in unique_names):
            unique_names.add(node.modified_path.absolute)
        else:
            raise Exception("""Naming conflict error.
            {0} cannot be renamed {1} since an item with the same name already exists.
            """.format(node.original_path.absolute, node.modified_path.absolute))

    def _check_existing_node(self, node, model):
        """Checks whether the modified node does not override an existing node."""
        if self._is_modified_node(node):
            return
        if os.path.exists(node.modified_path.absolute):
            error = """Conflict error: cannot rename {0} to {1}. The destination path is not empty.""".format(node.original_path.absolute, node.modified_path.absolute)
            conflicting_node = model.find_node_by_path(node.modified_path.absolute)
            if conflicting_node is None:
                # conflicting node is not part of the model.
                raise Exception(error)
            else:
                # Check whether the conflicting node was intended to be renamed
                if conflicting_node.modified_path.absolute is conflicting_node.original_path.absolute:
                    raise Exception(error)



class ActionCollection(object):
    def __init__(self):
        self._factory = ActionFactory()
        self._action_collection = list()

    def append(self, action_name, **parameters):
        action = self._factory.create(action_name, **parameters)
        self._action_collection.append(action)
        return action

    def insert(self, index, action_name, **parameters):
        action = self._factory.create(action_name, **parameters)
        self._action_collection.insert(action, index)
        return action

    def remove(self, index):
        return self._action_collection.pop(index)

    @property
    def items(self):
        return self._action_collection
