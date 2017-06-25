#!/usr/bin/python3

from enum import Enum


class EnumMask(Enum):
    """EnumFlags are only available in Python3.6
    so this is an implementation of it in the meantime.
    """

    def _create_composed_value(self, value):
        pseudo_member = object.__new__(self.__class__)
        pseudo_member._name_ = None
        pseudo_member._value_ = value
        return pseudo_member

    def get_enum(self, value):
        try:
            return self.__class__(value)
        except:
            return self._create_composed_value(value)

    def __or__(self, other):
        assert isinstance(other, Enum)
        return self.get_enum(self.value | other.value)

    def __and__(self, other):
        assert isinstance(other, Enum)
        return self.get_enum(self.value & other.value)

    def __contains__(self, other):
        assert isinstance(other, Enum)
        return self.value & other.value != 0
