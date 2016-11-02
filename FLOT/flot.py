import csv
import pathlib
import re
from channel import channel
from port import port
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

        _channelObj = None
        _modProdObj = None
        _portProdObj = None
        _modConsObj = None
        _portConsObj = None
        _channelObj = None

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
                print('---------------> Parsing issue on channel: '+_signal)

        # if signal field is empty this case is not possible => goto next line
        else:
            return None

        # if init field is not empty
        if _init:
            _channelObj.init = _init


        # is there a producer model:
        if _modOccProd:

            if _portProd:

                # we test first port cons dimension
                _testOnPort = re.match(r'(\w+)(?:\[(\d+)\])*', _portProd)

                if _testOnPort:

                    _portProd = _testOnPort.group(1)
                    _portProdIndex = _testOnPort.group(2)

                    # model object is created only if port is not null and succeed regexp test
                    # addModel method is also reference model object in flot object if not already defined
                    _modProdObj = self.addModel(modele(_modOccProd))

                    # create here producer port object
                    # addPort method is also reference port object in flot object if not already defined
                    _portProdObj = self.addPort(port(_portProd, _modProdObj.modocc), "producer")

                    # reference producer port object in model object
                    _modProdObj.addPort(_portProdObj)

                    # reference producer port object in channel object
                    _channelObj.addPort(_portProdObj)

                    # if a dimension is set on channel (signal)
                    if _portProdIndex:

                        # channel has no dimension yet, we initialise min and max to current index
                        if not _portProdObj.hasDimPort():
                            _portProdObj.tabMin = _portProdIndex
                            _portProdObj.tabMax = _portProdIndex

                        # a dimension is already set
                        # we have to compare current index to min and max channel index
                        else:

                            if _portProdObj.tabMax is not None:
                                if int(_portProdIndex) >= _portProdObj.tabMax:
                                    _portProdObj.tabMax = _portProdIndex

                            if _portProdObj.tabMin is not None:
                                if int(_portProdIndex) <= _portProdObj.tabMin:
                                    _portProdObj.tabMin = _portProdIndex

                else:
                    print('---------------> Parsing issue on producer port: ' +  _portProd)

                # there is an operator on producer port
                if _opProd:
                    _portProdObj.operator = _opProd

                # if channel has an init value set port default value to it
                if _channelObj.init is not None:
                    _portProdObj.init_default = _channelObj.init
            else:
                return None



        # is there a consumer model:
        if _modOccCons:

            if _portCons:

                # we test first port cons dimension
                _testOnPort = re.match(r'(\w+)(?:\[(\d+)\])*', _portCons)

                if _testOnPort:

                    _portCons = _testOnPort.group(1)
                    _portConsIndex = _testOnPort.group(2)

                    # model object is created only if port is not null and succeed regexp test
                    # addModel method is also reference model object in flot object if not already defined
                    _modConsObj = self.addModel(modele(_modOccCons))

                    # create here consumer port object
                    # addPort method is also reference port object in flot object if not already defined
                    _portConsObj = self.addPort(port(_portCons, _modConsObj.modocc), "consumer")

                    # reference consumer port object in model object
                    _modConsObj.addPort(_portConsObj)

                    # reference consumer port object in channel object
                    _channelObj.addPort(_portConsObj)

                    # if a dimension is set on channel (signal)
                    if _portConsIndex:

                        # channel has no dimension yet, we initialise min and max to current index
                        if not _portConsObj.hasDimPort():

                            _portConsObj.tabMin = _portConsIndex
                            _portConsObj.tabMax = _portConsIndex

                        # a dimension is already set
                        # we have to compare current index to min and max channel index
                        else:

                            if _portConsObj.tabMax is not None:
                                if int(_portConsIndex) >= _portConsObj.tabMax:
                                    _portConsObj.tabMax = _portConsIndex

                            if _portConsObj.tabMin is not None:
                                if int(_portConsIndex) <= _portConsObj.tabMin:
                                    _portConsObj.tabMin = _portConsIndex

                else:
                    print('---------------> Parsing issue on consumer port: ' + _portCons)

                # there is an operator on producer port
                if _opCons:
                    _portConsObj.operator = _opCons

                # if channel has an init value set port default value to it
                if _channelObj.init is not None:
                    _portConsObj.init_default = _channelObj.init

            else:
                return None

    def addChannel(self, channelObj):

        _identifier = channelObj.getIdentifier()

        if _identifier not in self.channel_ref.keys():
            self.channel_ref[_identifier] = channelObj

        return self.channel_ref[_identifier]


    def addModel(self, modelObj):
        _identifier = modelObj.getIdentifier()

        if _identifier not in self.models_ref.keys():
            self.models_ref[_identifier] = modelObj
        else:
            del modelObj

        return self.models_ref[_identifier]


    def addPort(self, portObj, portType):

        _identifier = portObj.getIdentifier()
        portObj.type = portType

        if portType == "producer":
            if _identifier not in self.producers_ref.keys():
                self.producers_ref[_identifier] = portObj

            return self.producers_ref[_identifier]

        elif portType == "consumer":
            if _identifier not in self.consumers_ref.keys():
                self.consumers_ref[_identifier] = portObj

            return self.consumers_ref[_identifier]


    def hasModele(self,modeleIdentifier):
        if modeleIdentifier in self.models_ref.keys():
            return True
        else:
            return False


    def hasPort(self,portIdentifier):
        if portIdentifier in self.consumers_ref.keys():
            return True
        elif portIdentifier in self.producers_ref.keys():
            return True
        else:
            return False