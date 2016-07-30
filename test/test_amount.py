from pynance.models import Security, USD, Amount
from nose.tools import *


class TestAmounts:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_amount_multiplication(self):
        one = Amount(1, USD)
        ten = Amount(10, USD)

        assert_equals(one * 5, Amount(5, USD))
        assert_equals(5 * one, Amount(5, USD))
        assert_equals(one * 5.001, Amount(5.001, USD))

        assert_equals(0.5 * ten, Amount(5, USD))
        assert_equals(ten * 0.4, Amount(4, USD))

    def test_amount_addition(self):
        one = Amount(1, USD)
        ten = Amount(10, USD)
        hundred = Amount(100, USD)
        thousand = Amount(1000, USD)

        assert_equals(one + ten + hundred + thousand, Amount(1111, USD))
        assert_equals(0 + one, one)
        assert_equals(one + 0, one)

        assert_equals(9 + one, ten)
        assert_equals(one + 9, ten)

        assert_equals(one + 0.001, Amount(1.001, USD))
        assert_equals(0.001 + one, Amount(1.001, USD))

    def test_amount_subtraction(self):
        one = Amount(1, USD)
        ten = Amount(10, USD)
        hundred = Amount(100, USD)
        thousand = Amount(1000, USD)

        assert_equals(thousand - hundred - ten - one, Amount(889, USD))

        assert_equals(0 - one, Amount(-1, USD))
        assert_equals(one - 0, one)

        assert_equals(hundred - thousand, Amount(-900, USD))

        assert_equals(ten - 9, one)
        assert_equals(11 - ten, one)

        assert_equals(one - 0.001, Amount(0.999, USD))
        assert_equals(0.001 - one, Amount(-0.999, USD))

    def test_amount_equality(self):
        assert_equals(Amount(10, USD), Amount(10, USD))
        assert_not_equals(Amount(10, USD), Amount(20, USD))

        assert_equals(Amount(10.001, USD), Amount(10.001, USD))
        assert_not_equals(Amount(10.001, USD), Amount(10.003, USD))
        assert_not_equals(Amount(10.001, USD), Amount(-10.001, USD))

    def test_amount_hash(self):
        amount_set = set()
        amount_set.add(Amount(10, USD))
        amount_set.add(Amount(10, USD))

        assert_equals(len(amount_set), 1)
