from cashmoney import Security, USD, Amount
from nose.tools import assert_equals, assert_not_equals

class TestSecurities:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_security_comparisons(self):
        assert_equals(Security("USD"), USD)
        assert_equals(Security("USD"), Security("USD"))
        assert_equals(Security("BTC"), Security("BTC"))

        assert_not_equals(Security("INR"), USD)
        assert_not_equals(Security("INR"), Security("BTC"))

    def test_security_hash(self):

        securities_set = set()
        securities_set.add(USD)
        securities_set.add(Security("USD"))
        securities_set.add(Security("USD"))
        assert_equals(len(securities_set), 1)

        securities_set.add(Security("BTC"))
        securities_set.add(Security("BTC"))
        assert_equals(len(securities_set), 2)

    def test_amount_addition(self):
        one = Amount(USD, 1)
        ten = Amount(USD, 10)
        hundred = Amount(USD, 100)
        thousand = Amount(USD, 1000)

        assert_equals(one + ten + hundred + thousand, Amount(USD, 1111))

    def test_amount_equality(self):
        assert_equals(Amount(USD, 10), Amount(USD, 10))
        assert_not_equals(Amount(USD, 10), Amount(USD, 20))

    def test_amount_hash(self):
        amount_set = set()
        amount_set.add(Amount(USD, 10))
        amount_set.add(Amount(USD, 10))

        assert_equals(len(amount_set), 1)
