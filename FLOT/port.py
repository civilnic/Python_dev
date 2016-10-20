class port:
    """
    Class to represent port in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, name):
        """
        Attributes are:
        _ path name of the file
        """
        self.name = name
        self.init_default = None
        self.type = None
        self.operator = None
        self.tabMin = None
        self.tabMax = None
        self.channel = None
        self.modocc = None


    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

    @property
    def init_default(self):
        return self.init_default

    @init_default.setter
    def init_default(self, init_default):
        self.init_default = init_default

    @property
    def type(self):
        return self.type

    @type.setter
    def type(self, type):
        self.type = type

    @property
    def operator(self):
        return self.operator

    @operator.setter
    def operator(self, operator):
        self.operator = operator

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
    def channel(self):
        return self.channel

    @channel.setter
    def channel(self, channel):
        self.channel = channel

    @property
    def modocc(self):
        return self.modocc

    @modocc.setter
    def modocc(self, modocc):
        self.modocc = modocc

    get