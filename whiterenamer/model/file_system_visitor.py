#!/usr/bin/python3

import abc
import action_descriptor
from file_node import FileNode
from folder_node import FolderNode


class FileSystemVisitor(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, file_system_tree_node):
        pass


class FileActionCollection(FileSystemVisitor, list):
    __metaclass__ = abc.ABCMeta

    def append_action(self, action_name, *parameters):
        file_system_action = self._create_action(action_name, *parameters)
        self.append(file_system_action)

    def remove_action_at(self, index):
        self.pop(index)

    def remove_action(self, file_system_action):
        self.remove(file_system_action)

    def _create_action(self, action_name, *parameters):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return action_instance


class FolderActionCollection(FileActionCollection):

    def __init__(self):
        super()

    def visit(self, folder_node):
        if(not isinstance(folder_node, FolderNode)):
            raise Exception("A Folder expected but something else was given.")
        modified_basename = ""
        for action in self._action_list:
            modified_basename += action.execute(folder_node.basename)


class FilenameActionCollection(FileActionCollection):

    def __init__(self):
        super()

    def visit(self, file_node):
        if(not isinstance(file_node, FileNode)):
            raise Exception("A FileNode expected but something else was given.")
        modified_basename = ""
        for action in self._action_list:
            modified_basename += action.execute(file_node.basename)
            file_node.basename = modified_basename


class ExtensionActionCollection(FileActionCollection):

    def __init__(self, action_list):
        super(action_list)

    def visit(self, file_node):
        modified_extension = ""
        for action in self._action_list:
            modified_extension += action.execute(file_node.extension)
            file_node.extension = modified_extension
