#!/usr/bin/python3

import os
import shutil
import uuid
from .filesystem.model import FileSystemModel, FilteredModel
from .action.factory import ActionFactory


class Renamer(object):
    def __init__(self, root_path, is_recursive=False, file_filter=None):
        self._original_model = FileSystemModel(root_path, is_recursive)
        self._filtered_model = FilteredModel(self._original_model, file_filter)
        self._action_collection = list()
        self._factory = ActionFactory()

    @property
    def filesystem_model(self):
        return self._filtered_model

    def update_model(self, file_filter):
        self._filtered_model = FileSystemModel(self._original_model, file_filter)

    @property
    def action_collection(self):
        return self._action_collection

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

    def invoke_actions(self):
        for filesystem_node in self._filtered_model.list_nodes():
            for action in self.action_collection:
                action.execute(filesystem_node)

    def batch_rename(self):
        self._verify_files_integrity()
        unprocessed_files = list(self._filtered_model.root_folder.children)
        for child in self._filtered_model.root_folder.children:
            child.rename()

    def _verify_files_integrity(self):
        """ Performs various tests to be sure that the renaming operations are safe."""
        unchecked_folders = list(self._original_model.root_folder)
        while len(unchecked_folders) > 0:
            folder = unchecked_folders.pop()
            folder._check_user_inputs()
            unchecked_folders.append(folder.get_folder_children())

    def _check_user_inputs(self):
        """ Specifies whether the user inputs does not lead to files with same names.
        """
        unique_names = set()
        for child_node in self.filtered_nodes:
            if (child_node.modified_path not in unique_names):
                unique_names.add(child_node.modified_path)
            else:
                raise Exception("""Naming conflict error.
                {0} cannot be renamed {1} since an item with the same name already exists.
                """.format(child_node.original_path, child_node.modified_path))

    def _check_conflicting_node(self):
        for child in self.filtered_nodes:
            if os.path.exists(child.modified_path):
                conflicting_node = self._filtered_model.find_node_by_path(child.modified_path)
                if conflicting_node is None:
                    continue
                else:
                    # If there is a conflicting node that must be renamed later,
                    # name it with a unique name to solve the issue.
                    # It will be renamed later anyway.
                    if conflicting_node.modified_name is "":
                        # This node is not intended to be renamed,
                        # so we'd better raise an exception
                        raise Exception("""The file/folder {0} cannot be renamed {1} since this path already exists.""".format(child.original_path, child.modified_path))
                    else:
                        conflicting_node = conflicting_node.original_name
                        temporary_name = uuid.uuid4()
                        conflicting_node.original_name.fullname = temporary_name
                        shutil.move(conflicting_node.original_path, conflicting_node.modified_path)


    def reset(self):
        """Reset the modified filedescriptor with the original one."""
        for node in self._all_nodes:
            node.reset()


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
