class port:
    """
    Class to represent port in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, name, modocc):
        """
        Attributes are:
        _ path name of the file
        """
        self._name = name
        self._modocc = modocc
        self._init_default = None
        self._type = None
        self._operator = None
        self._tabMin = None
        self._tabMax = None
        self._index = None
        self._channel = None

    @property
    def index(self):
        return self._index

    @index .setter
    def index(self, index):
        self._index = index

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def init_default(self):
        return self._init_default

    @init_default.setter
    def init_default(self, init_default):
        self._init_default = init_default

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator):
        self._operator = operator

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
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def modocc(self):
        return self._modocc

    @modocc.setter
    def modocc(self, modocc):
        self._modocc = modocc

    def getIdentifier(self):
        return str(self.modocc+"/"+self.name)

    def pprint(self):

        print(self.getIdentifier())
        print("\ttype: " + str(self.type))

        if self.init_default:
            print("\tinit_default: " + str(self.init_default))
        if self.operator:
            print("\toperator: " + str(self.operator))
        if self.tabMin is not None:
            print("\ttabMin: "+str(self.tabMin))
        if self.tabMin is not None:
            print("\ttabMax: "+str(self.tabMax))


    # method to know if a channel has a parameter tabMin or tabMax set
    # i.e. if a channel is more than dim 1
    # return type is a boolean
    def hasDimPort(self):
        if (self.tabMax is None) and (self.tabMin is None):
            return False
        else:
            return True