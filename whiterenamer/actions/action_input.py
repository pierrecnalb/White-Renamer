#!/usr/bin/python3


class ActionInput(object):
    """
    Describes a parameter from an action.
    Parameters:
        --parameter_name: string that represents the name given to the parameter described by this action input.
        --caption: string that represents the caption of the given parameter.
        --arg_type: specifies which type is the given parameter.
        --default_value: specifies the default value of the given parameter.
        --optional_argument: gives the possibility to add an optional argument for storing data.
    """

    def __init__(self, parameter_name, input_type):
        self._parameter_name = parameter_name
        self._input_type = input_type
        # Set the parameter name as default to caption.
        self._caption = parameter_name
        self._is_readonly = False
        self._is_visible = True

    @property
    def parameter_name(self):
        return self._parameter_name

    @parameter_name.setter
    def parameter_name(self, value):
        self._parameter_name = value

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, value):
        self._input_type = value

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def is_readonly(self):
        return self._is_readonly

    @is_readonly.setter
    def is_readonly(self, value):
        self._is_readonly = value

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, value):
        self._is_visible = value
