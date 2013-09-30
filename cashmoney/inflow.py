import time
import logging

class CashFlow(object):

    @staticmethod
    def init(args):
        return CashFlow.deserialize(args)

    @staticmethod
    def deserialize(args):
        if not "etime" in args: args["etime"] = None
        if not "last_withdrawn" in args: args["last_withdrawn"] = 0.0

        try:
            flow = CashFlow(args["name"], args["amount"], args["stime"], args["period"], args["etime"], args["last_withdrawn"])
        except KeyError as e:
            raise Exception("Unable to initialize CashFlow with args %s" %(str(args))) 

        return flow

    @staticmethod
    def serialize(flow):
        args = {}
        args["name"] = flow.name
        args["amount"] = flow.amount
        args["stime"] = flow.stime
        args["period"] = flow.period
        args["last_withdrawn"] = flow.last_withdrawn
        if flow.etime: args["etime"] = flow.etime
        return args
    
    def __init__(self, name, amount, stime, period, etime=None, last_withdrawn=0):
        self.name = name
        self.stime = stime
        self.period = period
        self.amount = amount
        self.log = logging.getLogger(__name__ + "." + self.name)

        self.etime = etime
        if not self.etime: self.etime = float("inf")

        self.last_withdrawn = last_withdrawn

    def __repr__(self):
        return "InFlow(name=%s, amount=%s, stime=%s, period=%s, etime=%s)" %(self.name, str(self.amount), str(self.stime), str(self.period), str(self.etime))

    def get(self):

        currtime = time.time()
        if currtime > self.etime:
            self.log.info("Can't get money anymore for %s" %(self))
            return 0.0

        if currtime < self.stime:
            self.log.info("Can't get money yet for %s" %(self))
            return 0.0

        duration = currtime - self.last_withdrawn
        if duration > self.period:
            self.last_withdrawn = time.time()
            self.log.info("Payday for %s" %(self))
            return self.amount

        return 0.0

