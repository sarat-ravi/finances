import logging

class Bank(object):

    def __init__(self, name, min_balance, balance):
        self.name = name
        self._balance = balance
        self.minimum_balance = min_balance
        self.inflows = {}

    @property
    def balance(self):
        return self._balance

    def __repr__(self):
        return "Bank(%s, balance=%s)" %(self.name, str(self.balance))

    def deposit(self, value):
        self._balance += value
        print "Added %s to balance %s" %(str(value), str(self._balance))

    def withdraw(self, value):
        if value > self._balance:
            print "Not enough funds"
            return

        self._balance -= value
        print "Removed %s to balance %s" %(str(value), str(self._balance))

        if self._balance < self.minimum_balance:
            print "Funds too low"

