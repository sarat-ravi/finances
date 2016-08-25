from pynance.market.model import MarketModel

class Market(object):
    """
    Determines the worth of a security in another security.
    """

    def __init__(self, name):
        self._name = name
        # TODO(Sarat): Support weighted market models.
        self._market_models = []

    def quote(amount, security, t):
        """
        Returns an amount that represents how much the specified amount is worth in the specified security at the specified t.
        """
        # TODO(Sarat): Support weighted market models.
        for market_model in self._market_models:
            if market_model.can_quote(amount.security, security, t):
                return market_model.quote(amount, security, t)



