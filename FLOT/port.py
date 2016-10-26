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
        self._channel = None

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
        self._tabMin = tabMin

    @property
    def tabMax(self):
        return self._tabMax

    @tabMax.setter
    def tabMax(self, tabMax):
        self._tabMax = tabMax

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
        print (self.getIdentifier())