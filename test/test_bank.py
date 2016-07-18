from cashmoney import BankAccount
from nose.tools import assert_equals

class TestBankAccount:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_basic_deposit(self):
        b = BankAccount('Wells Fargo', 100, 0)
        assert_equals(b.balance, 0)

        b.deposit(100)
        assert_equals(b.balance, 100)

    def test_basic_withdrawal(self):
        b = BankAccount('Wells Fargo', 100, 200)
        assert_equals(b.balance, 200)

        b.withdraw(100)
        assert_equals(b.balance, 100)

    def test_withdrawal_overdraft_prevention(self):
        b = BankAccount('Wells Fargo', 100, 200)
        assert_equals(b.balance, 200)

        b.withdraw(4000)
        assert_equals(b.balance, 200)

