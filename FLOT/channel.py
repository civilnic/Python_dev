class channel:
    """
    Class to represent channel in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, name):
        """
        Attributes are:
        _ path name of the file
        """
        self._name = name
        self._init = None
        self._tabMin = None
        self._tabMax = None
        self._ports_consum = []
        self._ports_prod = []


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def init(self):
        return self._init

    @init.setter
    def init(self, init):
        self._init = init

    @property
    def tabMin(self):
        return self._tabMin

    @tabMin.setter
    def tabMin(self, tabMin):
        self._tabMin = int(tabMin)

    @property
    def tabMax(self):
        return self._tabMax

    @tabMax.setter
    def tabMax(self, tabMax):
        self._tabMax = int(tabMax)

    @property
    def ports_consum(self):
        return self._ports_consum

    @ports_consum.setter
    def ports_consum(self, ports_consum):
        self._ports_consum.append(ports_consum)

    @property
    def ports_prod(self):
        return self._ports_prod

    @ports_prod.setter
    def ports_prod(self, ports_prod):
        self._ports_prod.append(ports_prod)

    def getIdentifier(self):
        return str(self._name)

    # method to know if a channel has a parameter tabMin or tabMax set
    # i.e. if a channel is more than dim 1
    # return type is a boolean
    def hasDimChannel(self):
        if (self.tabMax is None) and (self.tabMin is None):
            return False
        else:
            return True

    def pprint(self):
        print( "Channel Object: \n\t_name: "+self._name)
        if self._init:
            print( "\t_init: "+self._init)
        if self._tabMin:
            print( "\t_tabMin: "+str(self._tabMin))
        if self._tabMin:
            print( "\t_tabMax: "+str(self._tabMax))
