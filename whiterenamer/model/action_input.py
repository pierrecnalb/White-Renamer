#!/usr/bin/python3


class ActionInput(object):
    """
    Describes the inputs properties of the action.
    Parameters:
        --arg_name: string that represents the name of the given parameter.
        --arg_caption: string that represents the caption of the given parameter.
        --arg_type: specifies which type is the given parameter.
        --default_value: specifies the default value of the given parameter.
        --optional_argument: gives the possibility to add an optional argument for storing data.
    """

    def __init__(self,
                 arg_name,
                 arg_caption,
                 arg_type,
                 default_value):
        self._name = arg_name
        self._caption = arg_caption
        self._type = arg_type
        self.default_value = default_value
        self._value = default_value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, value):
        self._caption = value

    @property
    def input_type(self):
        return self._type

    @input_type.setter
    def input_type(self, value):
        self._type = value

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        self._default_value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
