class modele:
    """
    Class to represent modele in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, modocc):
        """
        Attributes are:
        _ path name of the file
        """
        self._modocc = modocc
        self._occurence = None
        self._name = None
        self._ports_consum = []
        self._ports_prod = []

    @property
    def modocc(self):
        return self._modocc

    @modocc.setter
    def modocc(self, modocc):
        self._modocc = modocc

    @property
    def occurence(self):
        return self._occurence

    @occurence.setter
    def occurence(self, occurence):
        self._occurence = occurence

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

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
        return str(self.modocc)

    def pprint(self):
        print("Modele name: "+self.modocc)

    def addPort(self, portObj):
        if portObj.type == "producer":
            if portObj not in self._ports_prod:
                self._ports_prod.append(portObj)
        elif portObj.type == "consumer":
            if portObj not in self._ports_consum:
                self._ports_consum.append(portObj)