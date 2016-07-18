

class Flow(object):

    def __init__(self, name):
        super(Flow, self).__init__()
        self.name = name

    def __repr__(self):
        return "Flow(name=%s)" %(self.name)

