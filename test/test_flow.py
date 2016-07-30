from pynance import PeriodicFlow
from pynance.models import Amount, USD
from nose.tools import assert_equals, assert_not_equals

class TestFlows:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_periodic_flow(self):
        amount = Amount(3, USD)
        flow = PeriodicFlow(name="testFlow", period=10, stime=5, etime=45, amount=amount)

        valid_range = range(5, 45, 10)
        for i in xrange(-1, 50):
            if i in valid_range:
                assert_equals(flow[i], amount)
            else:
                assert_equals(flow[i], 0)

    def test_adding_periodic_flows(self):
        five_amount = Amount(5, USD)
        ten_amount = Amount(10, USD)
        fifteen_amount = Amount(15, USD)

        flow = PeriodicFlow(name="fives", period=5, stime=3, etime=24, amount=five_amount)
        flow += PeriodicFlow(name="tens", period=10, stime=3, etime=45, amount=ten_amount)

        fifteen_expected = (3, 13, 23)
        five_expected = (8, 18)
        ten_expected = (33, 43)

        for i in xrange(-1, 50):
            amount = flow[i]
            if i in fifteen_expected:
                assert_equals(amount, fifteen_amount)
            elif i in five_expected:
                assert_equals(amount, five_amount)
            elif i in ten_expected:
                assert_equals(amount, ten_amount)
            else:
                assert_equals(amount, 0)

