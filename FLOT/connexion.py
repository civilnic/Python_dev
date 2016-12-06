from FLOT.port import port
from FLOT.channel import channel
from FLOT.alias import alias

class connexion:
    """
    Class to represent connexion in ASPIC, MEXICO or DSS data flot
    """

    def __init__(self):

        self._modoccProd = None
        self._portProd = None
        self._operatorProd = None
        self._tabProd = None
        self._Channel = None
        self._init = None
        self._modoccCons = None
        self._portCons = None
        self._operatorCons = None
        self._tabCons = None


    @property
    def modoccProd(self):
        return self._modoccProd

    @modoccProd.setter
    def modoccProd(self, modoccProd):
        self._modoccProd = modoccProd

    @property
    def portProd(self):
        return self._portProd

    @portProd.setter
    def portProd(self, portProd):
        self._portProd = portProd

    @property
    def operatorProd(self):
        return self._operatorProd

    @operatorProd.setter
    def operatorProd(self, operatorProd):
        self._operatorProd = operatorProd

    @property
    def tabProd(self):
        return self._tabProd

    @tabProd.setter
    def tabProd(self, tabProd):
        self._tabProd = tabProd

    @property
    def Channel(self):
        return self._Channel

    @Channel.setter
    def Channel(self, Channel):
        self._Channel = Channel

    @property
    def init(self):
        return self._init

    @init.setter
    def init(self, init):
        self._init = init

    @property
    def modoccCons(self):
        return self._modoccCons

    @modoccCons.setter
    def modoccCons(self, modoccCons):
        self._modoccCons = modoccCons


    @property
    def portCons(self):
        return self._portCons

    @portCons.setter
    def portCons(self, portCons):
        self._portCons = portCons

    @property
    def operatorCons(self):
        return self._operatorCons

    @operatorCons.setter
    def operatorCons(self, operatorCons):
        self._operatorCons = operatorCons

    @property
    def tabCons(self):
        return self._tabCons

    @tabCons.setter
    def tabCons(self, tabCons):
        self._tabCons = tabCons

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.modoccProd == other.modoccProd) and \
                    (self.portProd == other.portProd) and \
                    (self.operatorProd == other.operatorProd) and \
                    (self.tabProd == other.tabProd) and \
                    (self.Channel == other.Channel) and \
                    (self.init == other.init) and \
                    (self.modoccCons == other.modoccCons) and \
                    (self.portCons == other.portCons) and \
                    (self.operatorCons == other.operatorCons) and\
                    (self.tabCons == other.tabCons)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented


    def getTab(self):

        tab = []

        tab.append(self.modoccProd)
        tab.append(self.portProd)
        tab.append(self.operatorProd)
        tab.append(self.tabProd)
        tab.append(self.Channel)
        tab.append(self.init)
        tab.append(self.modoccCons)
        tab.append(self.portCons)
        tab.append(self.operatorCons)
        tab.append(self.tabCons)

        return tab

class connexionFromObj(connexion):
    """
    Connexion element created from  port and channel object
    """
    def __init__(self, producerObj=None, channelObj=None, consummerObj=None):

        connexion.__init__(self)

        self.modoccProd = producerObj.modocc
        self.portProd = producerObj.name
        self.operatorProd = producerObj.operator
        self.tabProd = None
        self.Channel = channelObj.name
        self.init = channelObj.init
        self.modoccCons = consummerObj.modocc
        self.portCons = consummerObj.name
        self.operatorCons = consummerObj.operator
        self.tabCons = None



class connexionFromAliasObj(connexion):

    def __init__(self, aliasProbObj, aliasConsObj):
        """
        Attributes are:
        _ path name of the file
        """

        connexion.__init__(self)

        if aliasProbObj.getChannelName == aliasConsObj.getChannelName:
            self.modoccProd = aliasProbObj.port.modocc
            self.portProd = aliasProbObj.port.name
            self.operatorProd = aliasProbObj.port.operator
            self.tabProd = aliasProbObj.index
            self.Channel = aliasProbObj.channel.name
            self.init = aliasProbObj.channel.init
            self.modoccCons = aliasConsObj.port.modocc
            self.portCons = aliasConsObj.port.name
            self.operatorCons = aliasConsObj.port.operator
            self.tabCons = aliasConsObj.index


class connexionFromTab(connexion):

    def __init__(self, tab):
        """
        Attributes are:
        _ path name of the file
        """

        connexion.__init__(self)

        if tab.len() == 10:
            self.modoccProd = tab[0]
            self.portProd = tab[1]
            self.operatorProd = tab[2]
            self.tabProd = tab[3]
            self.Channel = tab[4]
            self.init = tab[5]
            self.modoccCons = tab[6]
            self.portCons = tab[7]
            self.operatorCons = tab[8]
            self.tabCons = tab[9]

