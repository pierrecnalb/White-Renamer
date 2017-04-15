#!/usr/bin/python3

from action_descriptor import ActionDescriptor


class ActionDescriptorParser(object):
    """Parse all the ActionDescriptor objects."""

    def __init__(self):
        self.action_descriptors = [cls() for cls in ActionDescriptor.__subclasses__()]
