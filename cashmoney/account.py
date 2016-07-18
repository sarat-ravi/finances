from collections import defaultdict
from cashmoney.security import Security


class Lot(object):

    def __init__(self):
        self._securities_counter = defaultdict(int)

    def add_security(self, security, costbasis, t, amount):
        # TODO(Sarat): Implement this.
        self._securities_counter[security] += amount

    def remove_security(self, security, costbasis, t, amount):
        # TODO(Sarat): Implement this.
        self._securities_counter[security] -= amount

    def edit_lot(self, security, costbasis, t, new_amount):
        # TODO(Sarat): Implement this.
        self._securities_counter[security] = new_amount

    def get_total_amount_for_security(self, security):
        return self._securities_counter[security]


class Account(object):

    def __init__(self, name):
        super(Account, self).__init__()
        self._name = name
        self._lot = Lot()


class BrokerageAccount(Account):

    def __init__(self, name):
        super(BrokerageAccount, self).__init__(name=name)


class BankAccount(Account):

    def __init__(self, name, min_balance, balance):
        super(BankAccount, self).__init__(name=name)
        self._security_type = Security("USD")
        self._lot.add_security(self._security_type, 0, 0, balance)
        self.minimum_balance = min_balance

    @property
    def balance(self):
        return self._lot.get_total_amount_for_security(self._security_type)

    @balance.setter
    def balance(self, value):
        self._lot.edit_lot(self._security_type, 0, 0, value)

    def __repr__(self):
        return "BankAccount(%s, balance=%s)" %(self.name, str(self.balance))

    def deposit(self, value):
        self.balance += value

    def withdraw(self, value):
        if value > self.balance:
            print "Not enough funds"
            return

        self.balance -= value
        print "Removed %s to balance %s" %(str(value), str(self.balance))

        if self.balance < self.minimum_balance:
            print "Funds too low"

