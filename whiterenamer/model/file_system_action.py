#!/usr/bin/python3


class FileSystemAction(object):

    def __init__(self, action, apply_on_extension):
        self._action = action
        self._apply_on_extension

    @property
    def action(self):
        return self._action

    @property
    def apply_on_extension(self):
        return self._apply_on_extension
