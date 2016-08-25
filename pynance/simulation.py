from pynance.models import Account, Lot
from pynance.pipe import Pipe


class Simulation(object):
    """
    Class that captures a scenario that a user wants to simulate. For example, the user can construct a
    Simulation to plot the value of an account as time goes on, assuming an annual return of 6.00%
    """

    def __init__(self, name):
        self._name = name
        self._accounts = {}
        self._pipes = {}

    def add_account(self, account):
        assert isinstance(account, Account)
        self._accounts[account.name] = account

    def add_pipe(self, pipe):
        assert isinstance(account, Pipe)
        self._pipes[pipe.name] = pipe
