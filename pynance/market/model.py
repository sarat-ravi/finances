from pynance.models import Security, Amount

class MarketModel(object):
    """
    A market model that knows the answer to a question: How much is security A is worth in security B. Some models can be very specific,
    where the model only knows how to convert between MYR and USD, for example. Other models, on the other hand, can be more complex;
    for example, a CurrencyModel knows how to convert any currency into any other currency.
    """

    def __init__(self, name):
        self._name = name

    def can_quote(self, security_a, security_b, t):
        """
        Returns whether this model can tell how much Security A is worth in Security B
        """
        assert isinstance(security_a, Security)
        assert isinstance(security_b, Security)
        return self._can_quote(security_a, security_b, t)

    def quote(self, amount, security, t):
        """
        Returns an amount that represents how much the specified amount is worth in the specified security at the specified t.
        """
        assert isinstance(amount, Amount)
        assert isinstance(security, Security)
        return self._quote(amount, security, t)

    def _can_quote(self, security_a, security_b, t):
        raise NotImplementedError

    def _quote(self, amount, security, t):
        raise NotImplementedError

class StaticMarketModel(object):
    """
    A really stupid market model that assumes the value of security A is proportional to the value of security B, for any T.
    """

    def __init__(self, name, constant):
        super(LinearMarketModel, self).__init__(name)
        self._constant = constant

    def _can_quote(self, security_a, security_b, t):
        """Base Class Override"""
        # This dummy model simply uses a linear equation, so it can support anything.
        return True

    def _quote(self, amount, security, t):
        """Base Class Override"""
        # y = mx
        return Amount(amount.amount * self.constant, security)

class LinearMarketModel(object):
    """
    A really stupid market model that assumes the value of security A in terms of security B grows linearly as t goes on,
    independent of security A. As one can tell, this is a very useless model, but is useful for theoretical excercises.
    """

    def __init__(self, name, slope, initial_value):
        super(LinearMarketModel, self).__init__(name)
        self._slope = slope
        self._initial_value = initial_value

    def _can_quote(self, security_a, security_b, t):
        """Base Class Override"""
        # This dummy model simply uses a linear equation, so it can support anything.
        return True

    def _quote(self, amount, security, t):
        """Base Class Override"""
        # y = mt + b
        return Amount(self._slope * t, security) + Amount(self._initial_value, security)


