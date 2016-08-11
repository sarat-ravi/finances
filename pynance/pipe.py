from pynance.flow import Flow
from pynance.models import Account

class Pipe(object):
    # TODO(Sarat): Finish spec-ing this class

    def __init__(self, name, source_account=None, dest_account=None, flow):
        super(Pipe, self).__init__()
        self._name = name
        assert source_account == None or isinstance(source_account, Account)
        assert dest_account == None or isinstance(dest_account, Account)
        self._source_account = source_account
        self._dest_account = dest_account
        self._flow = flow

        self._blackouts = []
        self._last_flushed_t = None
        self._flow_enabled = False

    def start_flow(self, t)
        """
        Only flow after the specified t will actually be transferred from the source account to dest.
        """
        self._last_flushed_t = t
        self._flow_enabled = True

    def stop_flow(self, t)
        """
        Only flow after the specified t will actually be transferred from the source account to dest.
        """
        self._last_flushed_t = t
        self._flow_enabled = True

    def flush(self, t):
        """
        Will flush any of the flow from self._last_flushed_t to the specified t
        """
        for tt in xrange(self._last_flushed_t, t):
            amount = flow[tt]
            if amount:
                self._transfer(amount)

    def _transfer(self, amount):
        """
        Transfers the specified amount from the source account to the destination account.
        """
        raise NotImplementedError


