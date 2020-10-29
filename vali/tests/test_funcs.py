# encoding: utf-8

import unittest
from vali import validator, ValiFailError, ValiProp
from vali.funcs import *


@validator(valis=[LessThan(name='args', value=10)])
def less_than_test_func(args: int):
    pass


class TestLessThan(unittest.TestCase):
    def test_validate_pass(self):
        less_than_test_func(9)

    def test_validate_fail(self):
        self.assertRaises(ValiFailError, less_than_test_func, 11)


@validator(valis=[GreaterThan(name='args', value=20)])
def greater_than_test_func(args: int):
    pass


class TestGreaterThan(unittest.TestCase):
    def test_validate_pass(self):
        greater_than_test_func(100)

    def test_validate_fail(self):
        self.assertRaises(ValiFailError, greater_than_test_func, 0.0)


@validator(valis=[Range(name='args', value=(10, 20))])
def range_func(args: int):
    pass


@validator(valis=[Range(name='args', value=(None, 20))])
def range_func_with_end(args: int):
    pass


@validator(valis=[Range(name='args', value=(20, None))])
def range_func_with_start(args: int):
    pass


class TestRange(unittest.TestCase):
    def test_range_pass(self):
        range_func(10)
        range_func_with_start(30)
        range_func_with_end(10)

    def test_range_fail(self):
        self.assertRaises(ValiFailError, range_func, 9)
        self.assertRaises(ValiFailError, range_func, 20)
        self.assertRaises(ValiFailError, range_func_with_start, 10)
        self.assertRaises(ValiFailError, range_func_with_end, 30)


class RequireClass:
    required_attr = ValiProp([Required(name='required_attr', value=None)])
    non_required = None


class TestRequire(unittest.TestCase):
    def setUp(self):
        self.rc = RequireClass()

    def test_require_pass(self):
        self.rc.required_attr = 'success'
        self.rc.non_required = 'success too'

    def test_require_fail(self):
        self.assertRaises(ValiFailError, self.set_attr, self.rc)
        self.rc.non_required = None

    @staticmethod
    def set_attr(instance):
        print(instance.required_attr)
        instance.required_attr = None


@validator(valis=Include(name='age', value=[10, 20, 30]))
def include_test(age: int):
    pass


class TestInclude(unittest.TestCase):
    def test_include_pass(self):
        include_test(10)

    def test_include_fail(self):
        self.assertRaises(ValiFailError, include_test, 29)


@validator(valis=Exclude(name='age', value=[10, 20, 30]))
def include_test(age: int):
    pass


class TestInclude(unittest.TestCase):
    def test_include_pass(self):
        include_test(39)

    def test_include_fail(self):
        self.assertRaises(ValiFailError, include_test, 20)

if __name__ == '__main__':
    unittest.main()
