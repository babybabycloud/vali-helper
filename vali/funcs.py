# encoding: utf-8

from . import ValidationItem
from numbers import Number


class LessThan(ValidationItem):
    def __init__(self, name: str, value: Number):
        super().__init__(name=name, message="The validation value must less than {}", value=value)

    def validate(self, vali_value: Number) -> bool:
        return vali_value < self.value


class GreaterThan(ValidationItem):
    def __init__(self, name, value: Number):
        super().__init__(name=name, message="The validation value must greater than {}", value=value)

    def validate(self, vali_value: Number) -> bool:
        return vali_value > self.value