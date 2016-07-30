from cashmoney.models import Security, USD, Amount
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

