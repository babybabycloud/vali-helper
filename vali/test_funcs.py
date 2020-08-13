# encoding: utf-8

import unittest
from . import validator, ValiFailError
from .funcs import LessThan


@validator(vali_list=[LessThan('args', 10)])
def less_than_test_func(args: int):
    pass


class TestLessThan(unittest.TestCase):
    def test_validate_pass(self):
        less_than_test_func(9)

    def test_validate_fail(self):
        self.assertRaises(ValiFailError, less_than_test_func, 11)


if __name__ == '__main__':
    unittest.main()