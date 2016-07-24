from cashmoney import BankAccount
from nose.tools import assert_equals

class TestBankAccount:

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_basic_deposit(self):
        t = 0
        b = BankAccount('Wells Fargo', 100, 0, t)
        assert_equals(b.balance(t), 0)

        b.deposit(100, t+1)
        assert_equals(b.balance(t-10), 0)
        assert_equals(b.balance(t), 0)
        assert_equals(b.balance(t+1), 0)
        assert_equals(b.balance(t+2), 100)
        assert_equals(b.balance(t+10), 100)
        assert_equals(b.balance(t+100), 100)

    def test_basic_withdrawal(self):
        t = 0
        b = BankAccount('Wells Fargo', 100, 200, t)
        assert_equals(b.balance(t+1), 200)

        b.withdraw(100, t+1)
        assert_equals(b.balance(t+1), 200)
        assert_equals(b.balance(t+2), 100)
        assert_equals(b.balance(t+10), 100)
        assert_equals(b.balance(t+100), 100)

    def test_withdrawal_overdraft_prevention(self):
        t = 0
        b = BankAccount('Wells Fargo', 100, 200, t)
        assert_equals(b.balance(t), 0)
        assert_equals(b.balance(t+1), 200)

        b.withdraw(4000, t+1)
        assert_equals(b.balance(t+1), 200)
        assert_equals(b.balance(t+2), 200)
        assert_equals(b.balance(t+10), 200)
        assert_equals(b.balance(t+100), 200)

