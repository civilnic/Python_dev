from FLOT.port import port
from FLOT.channel import channel

class Alias:

    """
    Class to represent alias in ASPIC, MEXICO or DSS data flot
    """
    def __init__(self, port, channel, index=None, operator=None):
        """
        Attributes are:
        _ path name of the file
        """
        self._port = port
        self._index = index
        self._operator = operator
        self._channel = channel
        if self._port == self._channel:
            self._type = "default"
        else:
            self._type = "user"

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator):
        self._operator = operator

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index


    def getChannelName(self):
        return self.channel

    def getPortName(self):
        return self.port

    def getMexicoCpl(self):

        _channelField = self.channel

        if self.index:
            _channelField += "[" + str(self.index) + "]"

        if self.operator:
            _channelField += str(self.operator)

        return [self.port, _channelField]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.port == other.port) and \
                    (self.channel == other.channel) and \
                    (self.index == other.index) and \
                    (self.operator == other.operator)
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        else:
            return NotImplemented


class AliasObj(Alias):
    """
    Class to represent alias in ASPIC, MEXICO or DSS data flot
    """

    def __init__(self, portObj, channelObj,index=None, operator=None):

        Alias.__init__(portObj.name, channelObj.name, index, operator)


class MexicoAlias(Alias):
    """
    Class to represent alias in MEXICO data flot
    """
    def __init__(self, AliasObj=None, port=None, channel=None, index=None, operator=None,
                 sheet=None, date=None, comment=None):

        if AliasObj:
            Alias.__init__(AliasObj.port, AliasObj.channel, AliasObj.index, AliasObj.operator)
        else:
            Alias.__init__(port, channel, index, operator)

        self._sheet = sheet
        self._date = date
        self._comment = comment

    @property
    def sheet(self):
        return self._sheet

    @sheet.setter
    def sheet(self, sheet):
        self._sheet = sheet


    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment