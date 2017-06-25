#!/usr/bin/python3

from .descriptors import ActionDescriptor


class ActionFactory(object):
    """Parse all the ActionDescriptor objects."""

    def __init__(self):
        self._action_descriptors = {
            class_().name: class_()
            for class_ in ActionDescriptor.__subclasses__()
        }

    def create(self, name, **parameters):
        action_descriptor = self._action_descriptors[name]
        action_instance = action_descriptor.create_action(**parameters)
        return action_instance
