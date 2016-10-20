class modele:
    """
    Class to represent modele in ASPIC, MEXICO or DSS data flot
    """


    def __init__(self, modocc):
        """
        Attributes are:
        _ path name of the file
        """
        self.modocc = modocc
        self.occurence = None
        self.name = None
        self.ports_consum = []
        self.ports_prod = []

    @property
    def modocc(self):
        return self.modocc

    @modocc.setter
    def modocc(self, modocc):
        self.modocc = modocc

    @property
    def occurence(self):
        return self.occurence

    @occurence.setter
    def occurence(self, occurence):
        self.occurence = occurence

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name

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