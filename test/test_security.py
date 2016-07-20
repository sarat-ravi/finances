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
        one = Amount(1, USD)
        ten = Amount(10, USD)
        hundred = Amount(100, USD)
        thousand = Amount(1000, USD)

        assert_equals(one + ten + hundred + thousand, Amount(1111, USD))

    def test_amount_equality(self):
        assert_equals(Amount(10, USD), Amount(10, USD))
        assert_not_equals(Amount(10, USD), Amount(20, USD))

    def test_amount_hash(self):
        amount_set = set()
        amount_set.add(Amount(10, USD))
        amount_set.add(Amount(10, USD))

        assert_equals(len(amount_set), 1)
