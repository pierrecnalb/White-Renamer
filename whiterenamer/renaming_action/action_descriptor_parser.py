#!/usr/bin/python3

from action_descriptor import ActionDescriptor


class ActionDescriptorParser(object):
    """Parse all the ActionDescriptor objects."""

    def __init__(self):
        self._action_descriptors = {class_().name: class_() for class_ in ActionDescriptor.__subclasses__()}

    @property
    def find(self, name):
        return self._action_descriptors[name]
