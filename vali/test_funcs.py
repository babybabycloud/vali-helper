# encoding: utf-8

import unittest
from . import validator, ValiFailError
from .funcs import *


@validator(vali_list=[LessThan('args', 10)])
def less_than_test_func(args: int):
    pass


class TestLessThan(unittest.TestCase):
    def test_validate_pass(self):
        less_than_test_func(9)

    def test_validate_fail(self):
        self.assertRaises(ValiFailError, less_than_test_func, 11)


@validator(vali_list=[GreaterThan('args', 20)])
def greater_than_test_func(args: int):
    pass


class TestGreaterThan(unittest.TestCase):
    def test_validate_pass(self):
        greater_than_test_func(100)

    def test_validate_fail(self):
        self.assertRaises(ValiFailError, greater_than_test_func, 0.0)


@validator(vali_list=[Range('args', (10, 20))])
def range_func(args: int):
    pass


@validator(vali_list=[Range('args', (None, 20))])
def range_func_with_end(args: int):
    pass


@validator(vali_list=[Range('args', (20, None))])
def range_func_with_start(args: int):
    pass


class TestRange(unittest.TestCase):
    def test_range_pass(self):
        range_func(10)
        fange_func_with_start(30)
        fange_func_with_end(10)

    def test_range_pass(self):
        self.assertRaises(ValiFailError, range_func, 9)
        self.assertRaises(ValiFailError, range_func, 20)
        self.assertRaises(ValiFailError, range_func_with_start, 10)
        self.assertRaises(ValiFailError, range_func_with_end, 30)


if __name__ == '__main__':
    unittest.main()
