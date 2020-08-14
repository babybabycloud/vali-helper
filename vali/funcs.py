# encoding: utf-8

from . import ValidationItem
from numbers import Number
from typing import Any, Tuple


class LessThan(ValidationItem):
    def __init__(self, name: str, value: Number):
        super().__init__(name=name, message="The validation value must less than {}", value=value)

    def validate(self, vali_value: Number) -> bool:
        return vali_value < self.value


class GreaterThan(ValidationItem):
    def __init__(self, name: str, value: Number):
        super().__init__(name=name, message="The validation value must greater than {}", value=value)

    def validate(self, vali_value: Number) -> bool:
        return vali_value > self.value


class Range(ValidationItem):
    def __init__(self, name: str, value: Tuple[Number, Number]):
        super().__init__(name=name, message="The validation value must be in range {}", value=value)

    def validate(self, vali_value: Number) -> bool:
        begin = self.value[0]
        end = self.value[1]
        vali_result = False

        if begin != None:
            vali_result = vali_value >= begin
        if end != None:
            vali_result = vali_value < end if vali_result is True else False

        return vali_result


class Require(ValidationItem):
    def __init__(self, name: str):
        super().__init__(name=name, message="This attribute is required, can't be None", value=None)
    
    def validate(self, vali_value: Any) -> bool:
        return vali_value != self.value
