
class Security(object):

    def __init__(self, name):
        super(Security, self).__init__()
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return self._name == other._name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Security(%s)" %(self._name)


USD = Security("USD")

class Amount(object):

    def __init__(self, amount, security):
        super(Amount, self).__init__()
        self._security = security
        self._amount = amount

    def __eq__(self, other):
        return self._security == other._security and self._amount == other._amount

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self._security == USD:
            return "${}".format(self._amount)

        return "[{} {}]".format(self._amount, self._security)

    def __hash__(self):
        return hash((self._security, self._amount))

    def __radd__(self, other_value):
        return self + other_value

    def __add__(self, other_amount):
        if isinstance(other_amount, int) and other_amount == 0:
            return Amount(self._amount, self._security)

        if self._security != other_amount._security:
            raise ValueError("{} can't be added to {}".format(other_amount, self))

        return Amount(self._amount + other_amount._amount, self._security)


