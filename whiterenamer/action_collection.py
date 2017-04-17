#!/usr/bin/python3

from action_factory import ActionFactory


class ActionCollection(list):
    def append(self, action_name, **parameters):
        action = ActionFactory.create(action_name, **parameters)
        self.append(action)

    def insert(self, index, action_name, **parameters):
        action = ActionFactory.create(action_name, **parameters)
        self.insert(action, index)

    def remove(self, index):
        self.pop(index)
