#!/usr/bin/python3

import abc
from file_node import FileNode
from folder_node import FolderNode
import RenamingType


class FileSystemActionVisitor(list):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, file_system_tree_node):
        pass


class FolderActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, file_system_tree_node):
        if(not isinstance(file_system_tree_node, FolderNode)):
            return
        modified_basename = ""
        for action in self:
            modified_basename += action.execute(file_system_tree_node, RenamingType.basename)


class FileActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, file_system_tree_node):
        if(not isinstance(file_system_tree_node, FileNode)):
            return
        modified_basename = ""
        for action in self:
            modified_basename += action.execute(file_system_tree_node, RenamingType.basename)
            file_system_tree_node.basename = modified_basename


class ExtensionActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, file_system_tree_node):
        if(not isinstance(file_system_tree_node, FileNode)):
            return
        modified_extension = ""
        for action in self:
            modified_extension += action.execute(file_system_tree_node, RenamingType.extension)
            file_system_tree_node.extension = modified_extension
