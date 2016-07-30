from pynance.models.security import USD, Amount, Lot

class Account(object):

    def __init__(self, name):
        super(Account, self).__init__()
        self._name = name
        self._lot = Lot()

    def get_lot(self):
        return self._lot


class BrokerageAccount(Account):

    def __init__(self, name):
        super(BrokerageAccount, self).__init__(name=name)

    def add(self, spot, amount, t):
        assert isinstance(spot, Lot.Spot)
        self._lot.add(spot, amount, t)

    def remove(self, security, amount, t, mode):
        self._lot.remove(security, amount, t, mode)

    def get_total_amount_for_security(self, security, t):
        return self._lot.get_total_amount_for_security(security, t)


class BankAccount(Account):

    def __init__(self, name, min_balance, balance, t):
        super(BankAccount, self).__init__(name=name)
        self._security_type = USD
        self._lot.add(Lot.Spot(self._security_type, 0, t), balance, t)
        self.minimum_balance = min_balance

    def balance(self, t):
        return self._lot.get_total_amount_for_security(self._security_type, t)

    def __repr__(self):
        current_t = timer.time()
        return "BankAccount(%s, balance=%s, t=%s)" %(self.name, str(self.balance(t)), current_t)

    def deposit(self, amount, t):
        self._lot.add(Lot.Spot(self._security_type, 0, t), amount, t)

    def withdraw(self, amount, t):
        if amount > self.balance(t):
            print "Not enough funds"
            return

        self._lot.remove(self._security_type, amount, t, Lot.WITHDRAW_MODE_FIFO)
        print "Removed %s to balance %s" %(str(amount), str(self.balance(t)))

        if self.balance(t) < self.minimum_balance:
            print "Funds too low"

