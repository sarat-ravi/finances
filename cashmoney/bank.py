import logging

class Bank(object):

    @staticmethod
    def init(args):
        return Bank.deserialize(args)

    @staticmethod
    def deserialize(args):
        if not "min_balance" in args: args["min_balance"] = 100.0
        if not "balance" in args: args["balance"] = 0.0
        if not "meta" in args: args["meta"] = {}

        try:
            bank = Bank(args["name"], args["min_balance"], args["balance"], args["meta"])
        except KeyError as e:
            raise Exception("Unable to initialize bank with args %s" %(str(args))) 

        return bank

    @staticmethod
    def serialize(bank):
        args = {}
        args["name"] = bank.name
        args["balance"] = bank.balance
        args["min_balance"] = bank.minimum_balance
        args["meta"] = bank.meta
        return args

    def __init__(self, name, min_balance, balance, meta):
        self.name = name
        self._balance = balance
        self.meta = meta
        self.log = logging.getLogger(__name__ + "." + self.name)
        self.minimum_balance = min_balance
        self.inflows = {}

    @property
    def balance(self):
        self.poll_inflows()
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
        self.poll_inflows()

    def __repr__(self):
        return "Bank(%s, balance=%s)" %(self.name, str(self.balance))

    def poll_inflows(self):
        money = sum([inflow.get() for inflow_name, inflow in self.inflows.items()])
        self._balance += money
        self.log.info("got $%s from inflows, updating balance (%s)" %(str(money), str(self._balance)))

    def deposit(self, value):
        self.poll_inflows()

        self.balance += value
        self.log.info("Added %s to balance %s" %(str(value), str(self.balance)))

    def withdraw(self, value):
        self.poll_inflows()

        self.balance -= value
        self.log.info("Removed %s to balance %s" %(str(value), str(self.balance)))

        if self.balance < self.minimum_balance:
            self.log.critical("Funds too low")

    def add_inflow(self, inflow):
        self.inflows[inflow.name] = inflow
        self.log.info("Added inflow %s" %(str(inflow)))

