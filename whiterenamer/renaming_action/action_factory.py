#!/usr/bin/python3

from action_descriptor_parser import ActionDescriptorParser


class ActionFactory(object):

    @staticmethod
    def create(action_name, **parameters):
        action_descriptor = ActionDescriptorParser().find(action_name)
        for parameter_name, parameter_value in parameters.items():
            action_input = action_descriptor.inputs[parameter_name]
            action_input.value = parameter_value
        action_instance = action_descriptor.create_action()
        return action_instance
