import math

class Flow(object):

    def __init__(self, name):
        super(Flow, self).__init__()
        self.name = name

    def __repr__(self):
        return "Flow(name=%s)" %(self.name)

    def __getitem__(self, t):
        raise NotImplementedError

class PeriodicFlow(Flow):

    def __init__(self, name, period, amount, stime, etime=None):
        super(PeriodicFlow, self).__init__(name)
        self._stime = stime
        self._etime = etime
        self._period = period
        self._amount = amount

    def __contains__(self, t):
        return (t - self._stime) % self._period == 0 if self._is_within_bounds(t) else False

    def __getitem__(self, t):
        return self._amount if t in self else None

    def _is_within_bounds(self, t):
        return not ((self._stime and t < self._stime) or (self._etime and t >= self._etime))

