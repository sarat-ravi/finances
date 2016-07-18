
class Security(object):

    def __init__(self, name):
        super(Security, self).__init__()
        self._name = name

    def __hash__(self):
        return hash(self._name)

    def __repr__(self):
        return "Security(%s)" %(self._name)

