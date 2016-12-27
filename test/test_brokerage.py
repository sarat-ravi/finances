from pynance.models import BrokerageAccount, USD, INR, MYR, Lot, Amount
from nose.tools import assert_equals
from pynance.market import Market, StaticMarketModel 

class TestBrokerageAccount:

    def setup(self):
        pass

    def teardown(self):
        pass

    def assert_amounts(self, b, amounts, t):
        for security, amount in amounts:
            assert_equals(b.get_total_amount_for_security(security, t), amount)

    def assert_dicts(self, actual_dict, expected_dict):
        assert_equals(len(actual_dict), len(expected_dict))

        for key, expected_value in expected_dict.iteritems():
            assert_equals(actual_dict[key], expected_value)

    def test_getting_total_value_of_account(self):
        t = 0

        market = Market("NYSE")
        static_model = StaticMarketModel("multiplyByTenModel", 10)
        market.add_market_model(static_model, 1)

        b = BrokerageAccount('Schwab', market)
        b.add(Lot.Spot(USD, 0, t+1), 100, t+5)
        b.add(Lot.Spot(MYR, 1, t+1), 200, t+10)
        b.add(Lot.Spot(USD, 2, t+1), 300, t+20)
        b.add(Lot.Spot(MYR, 0, t+2), 400, t+30)
        b.add(Lot.Spot(USD, 0, t+2), 500, t+40)

        assert_equals(b.get_value_amount_of_account_in_security(USD, t=0), 0)
        assert_equals(b.get_value_amount_of_account_in_security(USD, t=6), Amount(100, USD))
        assert_equals(b.get_value_amount_of_account_in_security(USD, t=11), Amount(2100, USD))
        assert_equals(b.get_value_amount_of_account_in_security(USD, t=50), Amount(6900, USD))


    def test_getting_securities_counter_from_lot(self):
        t = 0
        spot_a = Lot.Spot(USD, 0, t+1)
        spot_b = Lot.Spot(MYR, 1, t+1)
        spot_c = Lot.Spot(USD, 2, t+1)
        spot_d = Lot.Spot(MYR, 0, t+2)
        spot_e = Lot.Spot(USD, 0, t+2)
        spot_f = Lot.Spot(INR, 3, t+3)

        b = BrokerageAccount('Schwab')
        b.add(spot_a, 100, t+5)
        b.add(spot_b, 200, t+5)
        b.add(spot_c, 300, t+5)
        b.add(spot_d, 400, t+5)
        b.add(spot_e, 500, t+5)
        b.add(spot_f, 600, t+5)

        expected_dict = {USD: 900, MYR: 600, INR: 600}
        self.assert_dicts(b.get_securities_dict(t=10), expected_dict)


    def test_adding_and_getting_lot_as_dict(self):
        t = 0
        # Spot can differ by both costbasis and by t!
        spot_a = Lot.Spot(USD, 0, t+1)
        spot_b = Lot.Spot(USD, 1, t+1)
        spot_c = Lot.Spot(USD, 2, t+1)
        spot_d = Lot.Spot(USD, 0, t+2)
        spot_e = Lot.Spot(USD, 0, t+2)

        b = BrokerageAccount('Schwab')
        b.add(spot_a, 100, t+5)
        b.add(spot_b, 200, t+5)
        b.add(spot_c, 300, t+5)
        b.add(spot_d, 400, t+5)
        b.add(spot_e, 500, t+5)

        expected_lot = {spot_a: 100, spot_b: 200, spot_c: 300, spot_d: 400, spot_e: 500}
        self.assert_dicts(b.get_lot_as_dict(t=10), expected_lot)

    def test_adding_and_getting_lot_as_dict(self):
        t = 0
        # Spot can differ by both costbasis and by t!
        spot_a = Lot.Spot(USD, 0, t+1)
        spot_b = Lot.Spot(MYR, 1, t+1)
        spot_c = Lot.Spot(USD, 2, t+2)
        spot_d = Lot.Spot(MYR, 0, t+2)
        spot_e = Lot.Spot(MYR, 0, t+2)
        spot_f = Lot.Spot(USD, 3, t+3)

        b = BrokerageAccount('Schwab')
        b.add(spot_a, 100, t+5)
        b.add(spot_b, 200, t+5)
        b.add(spot_c, 300, t+5)
        b.add(spot_d, 400, t+5)
        b.add(spot_e, 500, t+5)
        b.add(spot_f, 600, t+5)


        b.remove(USD, 50, t=10, mode=Lot.WITHDRAW_MODE_FIFO)

        # Test that the dict didn't change before the remove transaction was made
        expected_lot_in_past = {spot_a: 100, spot_b: 200, spot_c: 300, spot_d: 400, spot_e: 500, spot_f: 600}
        self.assert_dicts(b.get_lot_as_dict(t=10), expected_lot_in_past)

        # Test the dict's final state.
        expected_lot = {spot_a: 50, spot_b: 200, spot_c: 300, spot_d: 400, spot_e: 500, spot_f: 600}
        self.assert_dicts(b.get_lot_as_dict(t=20), expected_lot)

        b.remove(USD, 100, t=10, mode=Lot.WITHDRAW_MODE_FIFO)
        expected_lot = {spot_b: 200, spot_c: 250, spot_d: 400, spot_e: 500, spot_f: 600}
        self.assert_dicts(b.get_lot_as_dict(t=20), expected_lot)

        b.remove(USD, 50, t=10, mode=Lot.WITHDRAW_MODE_FIFO)
        expected_lot = {spot_b: 200, spot_c: 200, spot_d: 400, spot_e: 500, spot_f: 600}
        self.assert_dicts(b.get_lot_as_dict(t=20), expected_lot)

        b.remove(USD, 300, t=10, mode=Lot.WITHDRAW_MODE_FIFO)
        expected_lot = {spot_b: 200, spot_d: 400, spot_e: 500, spot_f: 500}
        self.assert_dicts(b.get_lot_as_dict(t=20), expected_lot)


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


