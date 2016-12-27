from pynance.market.market_model import MarketModel
from pynance.models.account import Amount
from pynance.models.security import MYR, Security
from decimal import Decimal

class Market(object):
    """
    Determines the worth of a security in another security.
    """

    def __init__(self, name):
        self._name = name
        self._market_models = {}

    def add_market_model(self, market_model, score):
        """
        Add a market model with an arbitrary user specified score, which measures the "legitimicy" of the model. All the scores
        for the models will be normalized and the weighted average will be used.
        """
        assert isinstance(market_model, MarketModel)
        self._market_models[market_model] = Decimal(score)

    def quote(self, amount, security, t):
        """
        Returns an amount that represents how much the specified amount is worth in the specified security at the specified t.
        """
        assert isinstance(amount, Amount)
        assert isinstance(security, Security)

        eligible_models = [(m, s) for (m, s) in self._market_models.iteritems() if m.can_quote(amount.security, security, t)]
        models = [m for m, _ in eligible_models]
        scores = [s for _, s in eligible_models]

        sum_scores = sum(scores)
        weights = [s/sum_scores for s in scores]

        value = 0
        for model, weight in zip(models, weights):
            value += model.quote(amount, security, t) * weight

        assert isinstance(value, Amount)
        return value

