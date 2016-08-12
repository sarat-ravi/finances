from pynance import Pipe, PeriodicFlow
from pynance.models import Amount, USD, Lot, BankAccount
from nose.tools import assert_equals, assert_not_equals

class TestPipes:

    def setup(self):
        pass

    def teardown(self):
        pass

    def _assert_amount(self, banks, amounts, t):
        for bank, amount in zip(banks, amounts):
            assert_equals(bank.balance(t), amount)

    def test_basic_functionality(self):
        t = 0
        amount = Amount(10, USD)
        flow = PeriodicFlow(name="testFlow", period=10, stime=5, etime=45, amount=amount)
        bank_a = BankAccount('Bank A', 100, 30, t)
        bank_b = BankAccount('Bank B', 100, 0, t)

        pipe = Pipe(name="testPipe", flow=flow, source_account=bank_a, dest_account=bank_b)

        pipe.start_flow(t)

        # Test that nothing gets tranfered for for T + 1 --> t + 4
        for i in range(1, 5):
            pipe.flush(t+i)
            self._assert_amount((bank_a, bank_b), (30, 0), t+i)

        pipe.flush(t+5)
        self._assert_amount((bank_a, bank_b), (30, 0), t+5)

        pipe.flush(t+6)
        self._assert_amount((bank_a, bank_b), (30, 0), t+6)
        self._assert_amount((bank_a, bank_b), (20, 10), t+7)


