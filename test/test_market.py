from pynance.models import Amount, Security, USD, MYR
from pynance.market import Market, StaticMarketModel
from nose.tools import assert_equals, assert_not_equals

class TestMarket:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_static_market(self):
        t = 0
        market = Market("NYSE")
        model_a = StaticMarketModel("10", 10)
        model_b = StaticMarketModel("100", 100)

        # model_a is twice as legit as model_b
        market.add_market_model(model_a, 2)
        market.add_market_model(model_b, 1)

        assert_equals(market.quote(Amount(2, USD), MYR, t+1), Amount(80, MYR))

