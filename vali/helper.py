# encoding: utf-8

from numbers import Number
from typing import Any

from .validation import ValidationItem, T


__all__ = [
    'LessThan',
    'GreaterThan',
    'Range',
    'Required',
    'Include',
    'Exclude',
    'Match',
    'Immutable'
]


class LessThan(ValidationItem):
    """
    Validate for if the value lesses than validation value
    """
    ERROR_MESSAGE = "less than"

    def test(self, vali_value: Number) -> bool:
        return vali_value < self.value


class GreaterThan(ValidationItem):
    """
    Validate for if the value greaters than validation value
    """
    ERROR_MESSAGE = "greater than"

    def test(self, vali_value: Number) -> bool:
        return vali_value > self.value


class Range(ValidationItem):
    """
    Validate for if the value is in a range. 
    [a, b) is the value could equal a, but cannot equal b.
    """
    ERROR_MESSAGE = "be in range"

    def test(self, vali_value: Number) -> bool:
        begin = self.value[0]
        end = self.value[1]
        result = False

        if begin != None and end != None:
            result = begin <= vali_value and vali_value < end
        elif begin != None:
            result = begin <= vali_value
        elif end != None:
            result = vali_value < end
        return result


class Required(ValidationItem):
    """
    Validate for a value cannot be None
    """
    ERROR_MESSAGE = "This attribute is required, can't be "

    def test(self, vali_value: Any) -> bool:
        return vali_value != self.value


class Include(ValidationItem):
    """
    Validate for the validation values contain the value
    """
    ERROR_MESSAGE = "be contained in"

    def test(self, vali_value: T) -> bool:
        return vali_value in self.value


class Exclude(ValidationItem):
    """
    Validate for the validation values don't contain the value
    """
    ERROR_MESSAGE = "shouldn't be contained in"

    def test(self, vali_value: T) -> bool:
        return vali_value not in self.value


class Match(ValidationItem):
    """
    Validate for a string can match a regular expression
    """
    ERROR_MESSAGE = "not match to"

    def test(self, vali_value: str) -> bool:
        """
        :param vali_value: A regular expression.
        """
        import re
        vali_c = re.compile(self.value)
        return vali_c.search(vali_value) != None

class Immutable:
    """
    Immutable is a descriptor helps to define an attribute of an instance of class to be immutable
    """
    def __set_name__(self, owner, name):
        self._name = '_' + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance, value):
        if instance.__dict__.get(self._name) is None:
            instance.__dict__[self._name] = value
        else:
            raise ValueError(f'{self._name[1:]} of {instance} is immutable')
