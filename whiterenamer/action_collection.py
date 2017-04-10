#!/usr/bin/python3

import action_descriptor
import Scope


class ActionCollection(list):

    def append(self, action_name, *parameters, scope=None, string_range=None):
        action = self._create_action(action_name, *parameters)
        self.append(action)
        return action

    def _create_action(self, action_name, *parameters, scope, string_range):
        action_descriptor_instance = action_descriptor.__dict__[action_name](*parameters)
        if(scope is not None):
            action_descriptor_instance.scope = scope
        if(string_range is not None):
            action_descriptor_instance.range = string_range
        action_instance = action_descriptor_instance.create_action()
        return action_instance
