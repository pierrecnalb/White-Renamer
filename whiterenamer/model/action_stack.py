#!/usr/bin/python3


class ActionStack(object):

    def __init__(self):
        self._action_stack = list()

    def append_action(self, action_descriptor):
        self._action_stack.append(action_descriptor)

    def insert_action(self, index, action_descriptor):
        self._action_stack.insert(index, action_descriptor)

    def remove_action(self, action_descriptor):
        self._action_stack.remove(action_descriptor)
