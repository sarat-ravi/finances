from cashmoney import PeriodicFlow, Amount, USD
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
                assert_equals(flow[i], None)

