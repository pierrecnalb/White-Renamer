#!/usr/bin/python3

import action_descriptor
import Scope


class ActionCollection(list):

    def append_action(self, action_name, *parameters):
        action = self._create_action(action_name, *parameters)
        self.append(action)

    # def remove_action_at(self, index, target):
    #     self.pop(index)

    # def remove_action(self, action, target):
    #     self.remove(action)

    def _create_action(self, action_name, *parameters):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        action_instance = action_descriptor_instance.create_action()
        return action_instance
