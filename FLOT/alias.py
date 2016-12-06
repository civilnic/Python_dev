from FLOT.port import port
from FLOT.channel import channel

class alias:
    """
    Class to represent alias in ASPIC, MEXICO or DSS data flot
    """

    def __init__(self, portObj, channelObj,index=None, operator=None):
        """
        Attributes are:
        _ path name of the file
        """
        self.port = portObj
        self.index = index
        self.operator = operator
        self.channel = channelObj
        if self.port.name == self.channel.name:
            self.type = "default"
        else:
            self.type = "user"

    @property
    def port(self):
        return self.port

    @port.setter
    def port(self, port):
        self.port = port

    @property
    def channel(self):
        return self.channel

    @channel.setter
    def channel(self, channel):
        self.channel = channel

    def getChannelName(self):
        return self.channel.name

    def getPortName(self):
        return self.port.name

    def getMexicoCpl(self):

        _channelField = channel.name

        if self.index:
            _channelField += "[" + str(self.index) + "]"

        if self.operator:
            _channelField += str(self.operator)

        return [self.port.name,_channelField]