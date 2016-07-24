import copy
import numbers
from collections import defaultdict

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
        self_copy._amount = self_copy._amount * value
        return self_copy

    def __radd__(self, other_value):
        return self + other_value

    def __rsub__(self, other_value):
        if isinstance(other_value, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = other_value - self_copy._amount
            return self_copy

        raise ValueError("Unsupported input {}".format(other_value))

    def __sub__(self, other_amount):
        if isinstance(other_amount, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = self_copy._amount - other_amount
            return self_copy

        neg = copy.deepcopy(other_amount)
        neg._amount = neg._amount * -1
        return self + neg

    def __add__(self, other_amount):
        if isinstance(other_amount, numbers.Number):
            self_copy = copy.deepcopy(self)
            self_copy._amount = self_copy._amount + other_amount
            return self_copy

        if self._security != other_amount._security:
            raise ValueError("{} can't be added to {}".format(other_amount, self))

        return Amount(self._amount + other_amount._amount, self._security)

class Lot(object):
    # TODO(Sarat): Reimplement this class using sqlite

    WITHDRAW_MODE_FIFO = "FIFO"
    WITHDRAW_MODE_EXACT = "EXACT"

    def __init__(self):
        self._data = defaultdict(int)

    def add_amount(self, security, costbasis, amount, t):
        self._data[(security, costbasis, t)] += amount

    def remove_amount(self, security, costbasis, amount, t, withdraw_mode):
        if withdraw_mode == Lot.WITHDRAW_MODE_EXACT:
            key = (security, costbasis, t)
            if not key in self._data:
                raise ValueError("Lot not found")

            current_amount = self._data[key]

            if amount > current_amount:
                raise ValueError("Amount to remove exceeds current amount")

            new_amount = current_amount - amount
            if new_amount == 0:
                del self._data[key]
                return

            self._data[key] = new_amount
        elif withdraw_mode == Lot.WITHDRAW_MODE_FIFO:
            matching_key = None
            for key, _ in self._data.iteritems():
                sec, cb, tt = key
                if security == sec and cb == costbasis and tt < t:
                    matching_key = key
                    break
            if matching_key:
                new_amount = self._data[matching_key] - amount
                self._data[matching_key] = new_amount


    def edit_lot(self, security, costbasis, new_amount, t):
        key = (security, costbasis, t)
        if not key in self._data:
            raise ValueError("Lot not found")

        self._data[key] = new_amount

    def get_total_amount_for_security(self, security, t):
        total_amount = 0
        for key, amount in self._data.iteritems():
            sec, _, tt = key
            if security == sec and tt < t:
                total_amount += amount

        return total_amount



