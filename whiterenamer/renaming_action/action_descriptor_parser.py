#!/usr/bin/python3

import action_descriptor
import inspect


class ActionDescriptorParser(object):
    """Parse all the ActionDescriptor objects."""

    def __init__(self):
        inspect.getmembers(action_descriptor, inspect.isclass)
