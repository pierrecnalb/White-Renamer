#!/usr/bin/python3

import action_descriptor
from file_system_visitor import FolderActionVisitor, FileActionVisitor, ExtensionActionVisitor
import RenamingType


class FileSystemActionCollection():

    def __init__(self):
        self._folder_action_visitor = FolderActionVisitor()
        self._file_action_visitor = FileActionVisitor()
        self._extension_action_visitor = ExtensionActionVisitor()

    @property
    def folder_action_visitor(self):
        return self._folder_action_visitor

    @property
    def file_action_visitor(self):
        return self._file_action_visitor

    @property
    def extension_action_visitor(self):
        return self._extension_action_visitor

    def append_action(self, renaming_type, action_name, *parameters):
        file_system_action = self._create_action(action_name, *parameters)
        if renaming_type == RenamingType.foldername:
            self._folder_action_visitor.appen(file_system_action)
        elif renaming_type == RenamingType.filename:
            self._file_action_visitor.appen(file_system_action)
        elif renaming_type == RenamingType.extension:
            self._extension_action_visitor.appen(file_system_action)

    # def remove_action_at(self, index, target):
    #     self.pop(index)

    # def remove_action(self, file_system_action, target):
    #     self.remove(file_system_action)

    def clear(self):
        self._folder_action_visitor = FolderActionVisitor()
        self._file_action_visitor = FileActionVisitor()
        self._extension_action_visitor = ExtensionActionVisitor()

    def _create_action(self, action_name, *parameters):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return action_instance
