# encoding: utf-8

from . import ValidationItem
from numbers import Number

class LessThan(ValidationItem):
    def __init__(self, name, value: Number):
        super().__init__(name=name, message="The validation value can't less than %s")
        self.value = value

    def validate(self, vali_value: Number):
        return vali_value < self.value