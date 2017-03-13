#!/usr/bin/python3
import action_descriptor
from file_system_action import FileSystemAction


class FileSystemActionCollection(object):

    def __init__(self):
        self._ordered_action_list = list()

    def append_action(self, action_name, *parameters, apply_on_extension=False):
        file_system_action = self._create_action(action_name, *parameters)
        self._ordered_action_list.append(file_system_action)
        return file_system_action

    def remove_action_at(self, index):
        self._ordered_action_list.pop(index)

    def remove_action(self, file_system_action):
        self._ordered_action_list.remove(file_system_action)

    def _create_action(self, action_name, *parameters, apply_on_extension=False):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return FileSystemAction(action_instance, apply_on_extension)
