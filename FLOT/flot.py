import csv
import pathlib
import re

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
        self.ports_conso = []
        self.ports_prod = []
        self.channels = []
        self.models = []
        self.models_ref = dict()
        self.channel_ref = dict()
        self.consumers_ref = dict()
        self.producers_ref = dict()

        self.parseMexicoFlot()

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

                _channelTabRef = self.addChannel(_signal)

                if _testOnSignal.group(2):
                    print (_testOnSignal.group(1))
                    print (_testOnSignal.group(2))
            else:
                print('--------------->PROBLEME')

        # if signal field is empty this case is not possible => goto next line
        else:
            return None


    def addChannel(self, channel):

        if channel in self.channel_ref.keys():
            myList=channel_ref[]