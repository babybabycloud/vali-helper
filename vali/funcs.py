# encoding: utf-8

from . import ValidationItem
from .validation import T
from numbers import Number
from typing import Any, Tuple, Iterable


class LessThan(ValidationItem):
    """
    Validate for if the value lesses than validation value
    """
    ERROR_MESSAGE = "less than"
    def __init__(self, name: str, value: Number):
        super().__init__(name=name, value=value)

    def validate(self, vali_value: Number) -> Tuple[bool, str]:
        result = vali_value < self.value
        return result, None if result else self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value)


class GreaterThan(ValidationItem):
    """
    Validate for if the value greaters than validation value
    """
    ERROR_MESSAGE = "greater than"
    def __init__(self, name: str, value: Number):
        super().__init__(name=name, value=value)

    def validate(self, vali_value: Number) -> Tuple[bool, str]:
        result = vali_value > self.value
        return result, None if result else self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value)


class Range(ValidationItem):
    """
    Validate for if the value is in a range. 
    [a, b) is the value could equal a, but cannot equal b.
    """
    ERROR_MESSAGE = "be in range"
    def __init__(self, name: str, value: Tuple[Number, Number]):
        super().__init__(name=name, value=value)

    def validate(self, vali_value: Number) -> Tuple[bool, str]:
        begin = self.value[0]
        end = self.value[1]
        result = False

        if begin != None and end != None:
            result = begin <= vali_value and vali_value < end
        elif begin != None:
            result = begin <= vali_value
        elif end != None:
            result = vali_value < end
        return result, None if result else self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value)


class Required(ValidationItem):
    """
    Validate for a value cannot be None
    """
    def __init__(self, name: str):
        super().__init__(name=name, value=None)
    
    def validate(self, vali_value: Any) -> Tuple[bool, str]:
        result = vali_value != self.value
        return result, None if result else "This attribute is required, can't be None"


class Include(ValidationItem):
    """
    Validate for the validation values contain the value
    """
    ERROR_MESSAGE = "be contained in"
    def __init__(self, name: str, values: Iterable[T]):
        super().__init__(name=name, value=values)

    def validate(self, vali_value: T) -> Tuple[bool, str]:
        result = vali_value in self.value
        return result, None if result else self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value)


class Exclude(ValidationItem):
    """
    Validate for the validation values don't contain the value
    """
    ERROR_MESSAGE = "not be contained in"
    def __init__(self, name: str, values: Iterable[T]):
        super().__init__(name=name, value=values)

    def validate(self, vali_value: T) -> Tuple[bool, str]:
        result = vali_value not in self.value
        return result, None if result else self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value)