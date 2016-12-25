import copy
import numbers
from collections import defaultdict
from decimal import Decimal

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
INR = Security("INR")
MYR = Security("MYR")

class Amount(object):

    def __init__(self, amount, security):
        super(Amount, self).__init__()
        self._security = security
        self._amount = Decimal(amount)

    @property
    def security(self):
        return self._security

    @property
    def amount(self):
        return self._amount

    def _is_fuzzy_equal(self, amount_a, amount_b):
        return int(round(amount_a * 100)) == int(round(amount_b * 100))

    def __lt__(self, other):
        if self == other:
            return False

        if other == 0:
            return self._amount < 0

        if not self._security == other._security:
            raise ValueError("Can't compare different securities ({}, {})".format(self._security, other._security))

        return self._amount < other._amount

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return self == other or self > other

    def __eq__(self, other):
        if other == 0:
            return self._amount == 0

        return self._security == other._security and self._is_fuzzy_equal(self._amount, other._amount)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self._security == USD:
            token = "$" if self._amount >= 0 else "-$"
            return "{}{}".format(token, abs(self._amount))

        return "[{} {}]".format(self._amount, self._security)

    def __hash__(self):
        return hash((self._security, self._amount))

    def __rmul__(self, value):
        return self * value

    def __mul__(self, value):
        if not isinstance(value, numbers.Number):
            raise ValueError("Can't multiply by {} because its an invalid type".format(value))

        self_copy = copy.deepcopy(self)
        self_copy._amount = self_copy._amount * Decimal(value)
        return self_copy

    def __radd__(self, other_value):
        return self + other_value

    def __rsub__(self, other_value):
        if isinstance(other_value, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = Decimal(other_value) - self_copy._amount
            return self_copy

        raise ValueError("Unsupported input {}".format(other_value))

    def __sub__(self, other_amount):
        if isinstance(other_amount, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = self_copy._amount - Decimal(other_amount)
            return self_copy

        neg = copy.deepcopy(other_amount)
        neg._amount = neg._amount * Decimal(-1)
        return self + neg

    def __add__(self, other_amount):
        if isinstance(other_amount, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = self_copy._amount + Decimal(other_amount)
            return self_copy

        if self._security != other_amount._security:
            raise ValueError("{} can't be added to {}".format(other_amount, self))

        self_copy = copy.deepcopy(self)
        self_copy._amount = self._amount + other_amount._amount
        return self_copy


class Lot(object):
    """
    A Lot can be thought of as a parking lot, where each parking spot can be thought of as 
    one category of assets, for tax purposes.
    """
    # TODO(Sarat): Reimplement this class using sqlite

    WITHDRAW_MODE_FIFO = "FIFO"
    WITHDRAW_MODE_EXACT = "EXACT"

    class _Transaction(object):
        """
        Simple struct-like class that captures both 'add' and 'remove' transactions in one
        object and has some helper properties.
        """
        def __init__(self, transaction_type, params):
            super(Lot._Transaction, self).__init__()
            self.transaction_type = transaction_type
            self.params = params

            self.t = params[2]
            self.security = params[0].security if self.transaction_type == "add" else params[0]
            self.amount = params[1]

        def is_add(self):
            return self.transaction_type == "add"

        def is_remove(self):
            return self.transaction_type == "remove"

        def get_spot(self):
            if not self.is_add():
                raise ValueError("Can only get spot for an add transaction")

            spot = self.params[0]
            assert isinstance(spot, Lot.Spot)
            return spot

    def __init__(self):
        super(Lot, self).__init__()
        self._transactions = []

    def get_lot_as_dict(self, t):
        """
        Return the lot as a dict of <Spot> ==> <Number> to describe how much amount is in every spot,
        until but not including the specified 't'.
        """
        lot = defaultdict(int)

        valid_transactions = [tran for tran in self._transactions if tran.t < t]
        add_transactions = [tran for tran in valid_transactions if tran.is_add()]
        remove_transactions = [tran for tran in valid_transactions if tran.is_remove()]

        for transaction in add_transactions:
            lot[transaction.get_spot()] += transaction.amount

        left_to_remove = defaultdict(int)
        for transaction in remove_transactions:
            left_to_remove[transaction.security] += transaction.amount

        fifo_sorted_spots = sorted(lot.keys(), cmp=lambda x, y: x.t - y.t)
        for spot in fifo_sorted_spots:
            to_remove = min(left_to_remove[spot.security], spot.amount) 
            lot[spot] -= to_remove
            left_to_remove[spot.security] -= to_remove
            assert left_to_remove[spot.security] >= 0
            if lot[spot] == 0:
                del lot[spot]

        return lot

    def add(self, spot, amount, t):
        """
        Add some amount to a specific spot, at a certain t.

        >>> lot = Lot()
        >>> lot.get_total_amount_for_security(USD, t=10)
        0
        >>> lot.add(Lot.Spot(security=USD, costbasis=0, t=4), 100, t=8) 
        >>> lot.get_total_amount_for_security(USD, t=10)
        100
        """
        assert amount >= 0
        transaction = Lot._Transaction("add", (spot, amount, t))
        self._transactions.append(transaction)

    def remove(self, security, amount, t, mode):
        """
        Remove some amount of a specific security at t, with the specified 'mode'. In the FIFO
        mode, for example, the security will be removed only from the spot that has the earliest 't'.

        >>> lot = Lot()
        >>> lot.add(Lot.Spot(security=USD, costbasis=0, t=4), 100, t=8) 
        >>> lot.get_total_amount_for_security(USD, t=10)
        100
        >>> lot.remove(security=USD, amount=50, t=9, mode=WITHDRAW_MODE_FIFO)
        >>> lot.get_total_amount_for_security(USD, t=10)
        50
        """
        assert amount >= 0
        assert amount <= self.get_total_amount_for_security(security, t)
        transaction = Lot._Transaction("remove", (security, amount, t, mode))
        self._transactions.append(transaction)

    def get_total_amount_for_security(self, security, t):
        """
        Get total amount of a security up to but not including t.

        >>> lot = Lot()
        >>> lot.add(Lot.Spot(security=USD, costbasis=0, t=4), 100, t=8) 
        >>> lot.get_total_amount_for_security(USD, t=10)
        100
        """
        valid_transactions = [tran for tran in self._transactions if tran.t < t and tran.security == security]
        balance = 0
        for transaction in valid_transactions:
            if transaction.is_add():
                balance = balance + transaction.amount
            else:
                balance = balance - transaction.amount
        return balance

    class Spot(object):
        """
        A spot contains information to categorize one or more assets for tax purposes.
        """

        def __init__(self, security, costbasis, t, flags=0):
            super(Lot.Spot, self).__init__()

            # information that uniquely describes this spot.
            self.security = security
            self.costbasis = costbasis
            self.t = t

            # misc flags
            self.flags = flags

        def __hash__(self):
            return hash((self.security, self.costbasis, self.t))

        def __repr__(self):
            return "Spot(sec={}, cb={}, t={}), flags={}".format(self.security, self.costbasis, self.t, self.flags)

