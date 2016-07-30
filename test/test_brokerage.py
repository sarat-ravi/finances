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

    def test_basic_lot_removal(self):
        t = 0
        b = BrokerageAccount('Schwab')
        b.add(Lot.Spot(USD, 0, t+1), 1000, t+1)
        b.add(Lot.Spot(INR, 0, t+1), 1000, t+1)
        self.assert_amounts(b, ((USD, 1000), (INR, 1000)), t+2)

        b.remove(USD, 100, t+2, Lot.WITHDRAW_MODE_FIFO)
        self.assert_amounts(b, ((USD, 1000), (INR, 1000)), t+2)
        self.assert_amounts(b, ((USD, 900), (INR, 1000)), t+3)

        b.remove(USD, 100, t+3, Lot.WITHDRAW_MODE_FIFO)
        self.assert_amounts(b, ((USD, 900), (INR, 1000)), t+3)
        self.assert_amounts(b, ((USD, 800), (INR, 1000)), t+4)

        b.remove(INR, 100, t+4, Lot.WITHDRAW_MODE_FIFO)
        self.assert_amounts(b, ((USD, 800), (INR, 1000)), t+4)
        self.assert_amounts(b, ((USD, 800), (INR, 900)), t+5)

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

        b.add(Lot.Spot(USD, 0, t+3), 50, t+3)
        self.assert_amounts(b, ((USD, 150), (INR, 200)), t+4)

        b.add(Lot.Spot(INR, 0, t+4), 50, t+4)
        self.assert_amounts(b, ((USD, 150), (INR, 250)), t+5)


