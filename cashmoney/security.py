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

    class Spot(object):

        def __init__(self, security, costbasis, t):
            super(Lot.Spot, self).__init__()
            self.security = security
            self.costbasis = costbasis
            self.t = t

        def __hash__(self):
            return hash((self.security, self.costbasis, self.t))

        def __repr__(self):
            return "Spot(sec={}, cb={}, t={})".format(self.security, self.costbasis, self.t)

    class _SpotDiff(object):

        def __init__(self, spot, amount):
            super(Lot._SpotDiff, self).__init__()
            self.spot = spot
            self.amount = amount

        def __radd__(self, other_value):
            return self + other_value

        def __add__(self, other_diff):
            if isinstance(other_diff, numbers.Number) and other_diff == 0:
                return copy.deepcopy(self)

            if self.spot != other_diff.spot:
                raise ValueError("Can't add diffs, because spots are different")

            self_copy = copy.deepcopy(self)
            self_copy.amount = self_copy.amount + other_diff.amount
            return self_copy

    class _Diff(object):

        def __init__(self, spot_diffs=[]):
            super(Lot._Diff, self).__init__()
            self.spot_diffs = defaultdict(int)
            for spot_diff in spot_diffs:
                self.spot_diffs[spot_diff.spot] += spot_diff

        def __radd__(self, other_value):
            return self + other_value

        def __add__(self, other_diff):
            if isinstance(other_diff, numbers.Number) and other_diff == 0:
                return copy.deepcopy(self)

            self_copy = copy.deepcopy(self)
            for other_spot, other_spot_diff in other_diff.spot_diffs.iteritems():
                self_copy.spot_diffs[other_spot] += other_spot_diff

            return self_copy

    def __init__(self):
        self.diffs = defaultdict(int)

    def add(self, spot, amount, t):
        diff = Lot._Diff((Lot._SpotDiff(spot, amount),))

        if amount < 0 and amount > self.get_total_amount_for_security(spot.security, t):
            raise ValueError("Unable to remove {} from {}".format(amount, spot))

        self.diffs[t] += diff

    def remove(self, security, amount, t, mode):
        if mode == Lot.WITHDRAW_MODE_EXACT:
            raise NotImplementedError

        spot = self._get_fifo_spot(security, t)
        self.add(spot, -1 * amount, t)

    def _get_fifo_spot(self, security, t):
        min_tt = t
        first_diff = None
        for tt, diff in self.diffs.iteritems():
            if tt <= t and self._contains_security_in_diff(security, diff):
                min_tt = tt
                first_diff = diff

        candidate_spots = []
        for spt, spt_diff in first_diff.spot_diffs.iteritems():
            if spt.security == security:
                candidate_spots.append(spt)

        min_cb_spt = candidate_spots[0]
        min_cb = min_cb_spt.costbasis
        for spt in candidate_spots:
            if spt.costbasis < min_cb:
                min_cb = spt.costbasis
                min_cb_spt = spt

        return min_cb_spt

    def _contains_security_in_diff(self, security, diff):
        for spt, spt_diff in diff.spot_diffs.iteritems():
            if spt.security == security:
                return True

        return False

    def get_total_amount_for_security(self, security, t):
        total_diff = 0

        for tt, diff in self.diffs.iteritems():
            if tt < t:
                total_diff += diff

        if total_diff == 0:
            return 0

        total_amount = 0
        for _, spot_diff in total_diff.spot_diffs.iteritems():
            if spot_diff.spot.security == security:
                total_amount += spot_diff.amount

        return total_amount


