class channel:
    """
    Class to represent channel in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, name):
        """
        Attributes are:
        _ path name of the file
        """
        self.name = name
        self.init = None
        self.tabMin = None
        self.tabMax = None
        self.ports_consum = []
        self.ports_prod = []


    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def init(self):
        return self.init

    @init.setter
    def init(self, init):
        self.init = init

    @property
    def tabMin(self):
        return self.tabMin

    @tabMin.setter
    def tabMin(self, tabMin):
        self.tabMin = tabMin

    @property
    def tabMax(self):
        return self.tabMax

    @tabMax.setter
    def tabMax(self, tabMax):
        self.tabMax = tabMax

    @property
    def ports_consum(self):
        return self.ports_consum

    @ports_consum.setter
    def ports_consum(self, ports_consum):
        self.ports_consum.append(ports_consum)

    @property
    def ports_prod(self):
        return self.ports_prod

    @ports_prod.setter
    def ports_prod(self, ports_prod):
        self.ports_prod.append(ports_prod)