import csv
import pathlib
import re
from channel import channel
import port
from modele import modele
import connexion

class flot:
    """
    Class to parse MEXICO, ASPIC or DSS flot data file
    """


    def __init__(self, flotFile):
        """
        Attributes are:
        _ path name of the file
        """
        self.pathName = flotFile
        self.models_ref = dict()
        self.channel_ref = dict()
        self.consumers_ref = dict()
        self.producers_ref = dict()

        self.parseMexicoFlot()

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


    @property
    def ports_prod(self):
        return self.ports_prod

    @ports_prod.setter
    def ports_prod(self, ports_prod):
        self.ports_prod.append(ports_prod)

    def parseMexicoFlot(self):

        file = open(self.pathName, "r")

        try:
            #
            # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
            #
            fieldnames = [
                'MOD_OCC_PROD',
                'PORT_PROD',
                'OP_PROD',
                'SIGNAL',
                'INIT',
                'OP_CONS',
                'MOD_OCC_CONS',
                'PORT_CONS'
                ]

            reader = csv.DictReader(file, delimiter=';',fieldnames=fieldnames)

            #
            # read data
            #
            for row in reader:
                self.ParseLine(row)

        finally:
            file.close()

    def ParseLine(self, row):

        _modOccProd = row['MOD_OCC_PROD']
        _portProd = row['PORT_PROD']
        _opProd = row['OP_PROD']
        _signal = row['SIGNAL']
        _init = row['INIT']
        _opCons = row['OP_CONS']
        _modOccCons = row['MOD_OCC_CONS']
        _portCons = row['PORT_CONS']

        # if signal field is not empty
        if _signal:

            _testOnSignal = re.match(r'(\w+)(?:\[(\d+)\])*', _signal)

            if _testOnSignal:

                _signal = _testOnSignal.group(1)
                _signalIndex = _testOnSignal.group(2)

                # create a channel object and
                # reference it n flot object
                _channelObj = self.addChannel(channel(_signal))

                # if a dimension is set on channel (signal)
                if _signalIndex:

                    # channel has no dimension yet, we initialise min and max to current index
                    if not _channelObj.hasDimChannel():
                        _channelObj.tabMin = _signalIndex
                        _channelObj.tabMax = _signalIndex

                    # a dimension is already set
                    # we have to compare current index to min and max channel index
                    else:

                        if _channelObj.tabMax is not None:
                            if int(_signalIndex) >= _channelObj.tabMax:
                                _channelObj.tabMax = _signalIndex

                        if _channelObj.tabMin is not None:
                            if int(_signalIndex) <= _channelObj.tabMin:
                                _channelObj.tabMin = _signalIndex

            else:
                print('--------------->PROBLEME')

        # if signal field is empty this case is not possible => goto next line
        else:
            return None

        # if init field is not empty
        if _init:
            _channelObj.init=_init


        # is there a producer model:
        if _modOccProd:
            _modProdObj=self.addModel(modele(_modOccProd))


    def addChannel(self, channelObj):

        _identifier=channelObj.getIdentifier()

        if _identifier not in self.channel_ref.keys():
            self.channel_ref[_identifier]=channelObj

        return self.channel_ref[_identifier]


    def addModel(self, modelObj):
        _identifier = modelObj.getIdentifier()

        if _identifier not in self.models_ref.keys():
            self.models_ref[_identifier] = modelObj

        return self.models_ref[_identifier]