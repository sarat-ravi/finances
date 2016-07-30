import math
import copy

class Flow(object):

    def __init__(self, name, flows=[]):
        super(Flow, self).__init__()
        self.name = name
        self._flows = flows

    def __repr__(self):
        return "Flow(name=%s)" %(self.name)

    def __getitem__(self, t):
        return sum((flow[t] for flow in self._flows)) + self._get_item_for_self(t)

    def __add__(self, other_flow):
        self_copy = copy.deepcopy(self)
        self_copy._flows.append(other_flow)
        return self_copy

    def __contains__(self, t):
        return any((t in flow for flow in self._flows)) or self._contains_in_self(t)

    def _get_item_for_self(self, t):
        raise NotImplementedError

    def _contains_in_self(self, t):
        raise NotImplementedError

class PeriodicFlow(Flow):

    def __init__(self, name, period, amount, stime, etime=None):
        super(PeriodicFlow, self).__init__(name)
        self._stime = stime
        self._etime = etime
        self._period = period
        self._amount = amount

    def _contains_in_self(self, t):
        return (t - self._stime) % self._period == 0 if self._is_within_bounds(t) else False

    def _get_item_for_self(self, t):
        return self._amount if self._contains_in_self(t) else 0

    def _is_within_bounds(self, t):
        return not ((self._stime and t < self._stime) or (self._etime and t >= self._etime))

