from pynance.models import Amount, Security, USD, MYR
from pynance.market import Market, StaticMarketModel, LinearMarketModel
from nose.tools import assert_equals, assert_not_equals

class TestMarket:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_static_market_model(self):
        t = 0
        market = Market("NYSE")
        model_a = StaticMarketModel("10", 10)
        model_b = StaticMarketModel("100", 100)

        # model_a is twice as legit as model_b
        market.add_market_model(model_a, 2)
        market.add_market_model(model_b, 1)

        assert_equals(market.quote(Amount(2, USD), MYR, t+1), Amount(80, MYR))

    def test_linear_market_model(self):
        t = 0
        market = Market("NYSE")
        model = LinearMarketModel("y=2t+3", slope=2, initial_value=3)
        market.add_market_model(model, 10)

        for i in range(20):
            assert_equals(market.quote(Amount(7, USD), MYR, t+i), Amount(2*i + 3, MYR))


