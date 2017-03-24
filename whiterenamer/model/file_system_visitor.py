#!/usr/bin/python3

import abc
from file_node import FileNode
from folder_node import FolderNode


class FileSystemActionVisitor(list):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def visit(self, file_system_tree_node):
        pass


class FolderActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, folder_node):
        if(not isinstance(folder_node, FolderNode)):
            raise Exception("A Folder expected but something else was given.")
        modified_basename = ""
        for action in self:
            modified_basename += action.execute(folder_node.basename)


class FileActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, file_node):
        if(not isinstance(file_node, FileNode)):
            raise Exception("A FileNode expected but something else was given.")
        modified_basename = ""
        for action in self:
            modified_basename += action.execute(file_node.basename)
            file_node.basename = modified_basename


class ExtensionActionVisitor(FileSystemActionVisitor):

    def __init__(self):
        super()

    def visit(self, file_node):
        modified_extension = ""
        for action in self:
            modified_extension += action.execute(file_node.extension)
            file_node.extension = modified_extension
