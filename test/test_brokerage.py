from cashmoney import BrokerageAccount, USD, INR, Lot
from nose.tools import assert_equals

class TestBrokerageAccount:

    def setup(self):
        pass

    def teardown(self):
        pass

    def assert_amounts(self, b, amounts, t):
        for security, amount in amounts:
            assert_equals(b.get_total_amount_for_security(security, t), amount)


    def test_basic_lot_addition(self):
        t = 0
        b = BrokerageAccount('Schwab')
        
        self.assert_amounts(b, ((USD, 0), (INR, 0)), t)

        b.add(Lot.Spot(USD, 0, t+1), 100, t+1)
        self.assert_amounts(b, ((USD, 0), (INR, 0)), t+1)
        self.assert_amounts(b, ((USD, 100), (INR, 0)), t+2)

        b.add(Lot.Spot(INR, 0, t+1), 200, t+2)
        self.assert_amounts(b, ((USD, 0), (INR, 0)), t+1)
        self.assert_amounts(b, ((USD, 100), (INR, 0)), t+2)
        self.assert_amounts(b, ((USD, 100), (INR, 200)), t+3)


