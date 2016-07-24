from cashmoney.security import USD, Amount, Lot

class Account(object):

    def __init__(self, name):
        super(Account, self).__init__()
        self._name = name
        self._lot = Lot()

class BrokerageAccount(Account):

    def __init__(self, name):
        super(BrokerageAccount, self).__init__(name=name)


class BankAccount(Account):

    def __init__(self, name, min_balance, balance, t):
        super(BankAccount, self).__init__(name=name)
        self._security_type = USD
        self._lot.add_amount(self._security_type, 0, balance, t)
        self.minimum_balance = min_balance

    def balance(self, t):
        return self._lot.get_total_amount_for_security(self._security_type, t)

    def __repr__(self):
        current_t = timer.time()
        return "BankAccount(%s, balance=%s, t=%s)" %(self.name, str(self.balance(t)), current_t)

    def deposit(self, value, t):
        self._lot.add_amount(self._security_type, 0, value, t)

    def withdraw(self, value, t):
        if value > self.balance(t):
            print "Not enough funds"
            return

        self._lot.remove_amount(self._security_type, 0, value, t, Lot.WITHDRAW_MODE_FIFO)
        print "Removed %s to balance %s" %(str(value), str(self.balance(t)))

        if self.balance(t) < self.minimum_balance:
            print "Funds too low"

