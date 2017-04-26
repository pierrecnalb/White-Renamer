#!/usr/bin/python3

from .filesystem.model import Model
from .actions.factory import ActionFactory


class Renamer(object):
    def __init__(self, root_path, is_recursive=False, file_filter=None):
        self._model = Model(root_path, is_recursive, file_filter)
        self._action_collection = list()
        self._factory = ActionFactory

    @property
    def model(self):
        return self._model

    @property
    def action_collection(self):
        return self._action_collection

    def append(self, action_name, **parameters):
        action = self._factory.create(action_name, **parameters)
        self.append(action)
        return action

    def insert(self, index, action_name, **parameters):
        action = self._factory.create(action_name, **parameters)
        self.insert(action, index)
        return action

    def remove(self, index):
        return self.pop(index)

    def invoke_actions(self):
        for filesystem_node in self._model.filtered_nodes:
            for action in self.action_collection:
                action.execute(filesystem_node)

    def batch_rename(self):
        for node in self._all_nodes:
            node.rename()

    def reset(self):
        """Reset the modified filedescriptor with the original one."""
        for node in self._all_nodes:
            node.reset()
