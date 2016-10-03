import sys
import re
from A429 import (A429LabelBNR,A429LabelBCD,A429LabelHYB,A429LabelDIS)

class BDS:
    """
    Class to defined BDS data file
    """

    def __init__(self,path_name):
        """
        Attributes are:
        _ path name of the file
        """
        self.PathName=path_name
        self.BDS={}

    def add_system(self,system):
        if system not in self.BDS.keys():
            self.BDS[system]={}
            self.BDS[system]['LabelsList']=[]
            self.BDS[system]['SignalList'] = []

    def add_Label(self,system,LabelNumber,LabelOject):
        self.BDS[system]['LabelsList'].append((LabelNumber,LabelOject))

    def add_Signal(self,system, SignalName,LabelNumber):
        self.BDS[system]['SignalList'].append((SignalName,LabelNumber))

    def get_LabelObject(self,LabelNumber):
        if self.LabelsList.__len__()==0:
            return None
        else:
            LabelObj=None
            for label in self.LabelsList:
                if(label[0]==LabelNumber):
                    LabelObj=label[1]
            return LabelObj

    def parse_BDS(self):
        """
        Method to analyse BDS file
        """

        #
        # open file and apply first treatment
        # the original BDS file is on one line
        # the first substitution is to locate end of line
        #   _ reg exp is locating the following sequence:
        #    A4XLEACDT.1     021186  154046
        #    var_name        some_number some_number
        #    it replaces this sequence in line1 variable with:
        #    !A4XLEACDT.1     021186  154046
        # then file content is splitted with this character '!'
        # into several line on  BDSFILE_LIST variable
        #
        try:
            BDSFILE=open(self.PathName,'r')

        except IOError:
            print('cannot open', self.PathName)
        else:
                line = BDSFILE.readline()
                line1 = re.sub('(\\s*)([A-Z0-9_.]+\\s+[0-9]+  [0-9]+  )', '!\\2', line)
                BDSFILE_LIST = re.split('!', line1)

        #
        # each line of input BDS file is arround 618 bytes
        # the file is split with the following bytes numbers (keys of the dictionary)
        #
        BDS_Parameters=\
        {
            'IDENTIFICATOR':(0,16),
            'SYSTEM': (32, 36),
            'NATURE':(36,42),
            'TYPE NAME': (42, 54),
            'LABEL OUT': (54, 57),
            'SDI OUT': (57, 59),
            'BIT OUT': (59, 61),
            'INPUT TYPE EXTENSION':(61, 66),
            'INPUT PINS': (66, 96),
            'SOURCE OR UPSTREAM COMPUTER NAME': (96, 108),
            'OUTPUT TRANSMIT INTERVAL': (120, 129),
            'SIGNIFICANTS BITS': (129, 131),
            'RANGE MAX': (131, 144),
            'RESOLUTION': (144, 152),
            'UNIT': (152, 160),
            'FORMAT': (160, 164),
            'FILTER TIME CONSTANT': (164, 167),
            'PARAMETER DEFINITION': (167, 207),
            'LABEL IN': (207, 210),
            'SDI IN': (210, 212),
            'BIT IN': (212, 214),
            'INPUT TRANSMIT INTERVAL MIN/MAX': (214, 223),
            'FULL SCALE CODING ACCURACY':(223, 229),
            'ORIGIN ATA': (229, 234),
            'LIGHTING STRIKE PROTECTION': (236, 239),
            'COMMENTS': (255, 295),
            'STATE 1 PARAMETER DEFINITION': (417, 457),
            'STATE 0 PARAMETER DEFINITION OUT': (457, 502),
            'OUTPUT PINS': (512, 522)
        }

        bds_complete_map = \
        {
            1: 'IDENTIFICATOR',
            17: 'UNDEFINED1',
            25: 'UNDEFINED2',
            33: 'UNDEFINED3',
            37: 'NATURE',
            43: 'TYPE NAME',
            55: 'LABEL OUT',
            58: 'SDIOUT',
            60: 'BIT OUT',
            62: 'INPUT TYPE EXTENSION',
            67: 'INPUT PINS',
            97: 'SOURCE OR UPSTREAM COMPUTER NAME',
            109: 'UNDEFINED4',
            121: 'OUTPUT TRANSMIT INTERVAL',
            130: 'SIGNIFICANTS BITS',
            132: 'RANGE MAX',
            145: 'RESOLUTION',
            153: 'UNIT',
            161: 'FORMAT',
            165: 'FILTER TIME CONSTANT',
            168: 'PARAMETER DEFINITION',
            208: 'LABEL IN',
            211: 'SDI IN',
            213: 'BIT IN',
            215: 'INPUT TRANSMIT INTERVAL MIN/MAX',
            224: 'FULL SCALE CODING ACCURACY',
            230: 'ORIGIN ATA',
            235: 'UNDEFINED5',
            237: 'LIGHTING STRIKE PROTECTION',
            240: 'UNDEFINED6',
            256: 'COMMENTS',
            296: 'STATE 1 PARAMETER DEFINITION',
            336: 'STATE 0 PARAMETER DEFINITION',
            388: 'UNDEFINED7',
            398: 'OUTPUT BUS NAME',
            418: 'STATE 1 PARAMETER DEFINITION OUT',
            458: 'STATE 0 PARAMETER DEFINITION OUT',
            503: 'OUTPUT TYPE EXTENSION',
            513: 'OUTPUT PINS',
            523: 'UNDEFINED10',
            579: 'UNDEFINED11'
        }



        for line in BDSFILE_LIST:

            DicoLine = {}
            LabelObj = None
            for field in BDS_Parameters.keys():
                DicoLine[field]=line[BDS_Parameters[field][0]:BDS_Parameters[field][1]].strip()

            system=DicoLine['SYSTEM']
            self.add_system(system)

            nature=DicoLine['NATURE']

            if(nature == "ENTREE"):
                LabelObj = AddInputLabel(DicoLine)
                self.add_Label(system,LabelObj.number,LabelObj)

            elif (nature == "SORTIE"):
                LabelObj = AddOutputLabel(DicoLine)
                self.add_Label(system,LabelObj.number, LabelObj)

            elif (nature == "E/S"):
                LabelObj = AddInputLabel(DicoLine)
                self.add_Label(system,LabelObj.number,LabelObj)
                LabelObj = AddOutputLabel(DicoLine)
                self.add_Label(system,LabelObj.number, LabelObj)
            #else:
                #print("Label nature not defined:"+nature)




def AddInputLabel(DicoLine):

    LabelObj=None
#    print (DicoLine)

    if (DicoLine["FORMAT"]):
        if (DicoLine["FORMAT"] == "BNR"):
            LabelObj = A429LabelBNR(DicoLine["LABEL IN"], DicoLine["SDI IN"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        if (DicoLine["FORMAT"] == "BCD"):
            LabelObj = A429LabelBCD(DicoLine["LABEL IN"], DicoLine["SDI IN"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        if (DicoLine["FORMAT"] == "HYB"):
            LabelObj = A429LabelHYB(DicoLine["LABEL IN"], DicoLine["SDI IN"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        LabelObj.accuracy=DicoLine["FULL SCALE CODING ACCURACY"]

    # in case of DIS A429 label FORMAT field is empty
    else:
        LabelObj = A429LabelDIS(DicoLine["LABEL IN"], DicoLine["SDI IN"])

    LabelObj.input_trans_rate = DicoLine["INPUT TRANSMIT INTERVAL MIN/MAX"]
    LabelObj.originATA = DicoLine["ORIGIN ATA"]
    LabelObj.pins = DicoLine["INPUT PINS"]
    LabelObj.source = DicoLine["SOURCE OR UPSTREAM COMPUTER NAME"]
    LabelObj.nature = DicoLine['NATURE']

    return LabelObj

def AddOutputLabel(DicoLine):

    LabelObj=None

    if (DicoLine["FORMAT"]):
        if (DicoLine["FORMAT"] == "BNR"):
            LabelObj = A429LabelBNR(DicoLine["LABEL OUT"], DicoLine["SDI OUT"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        if (DicoLine["FORMAT"] == "BCD"):
            LabelObj = A429LabelBCD(DicoLine["LABEL OUT"], DicoLine["SDI OUT"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        if (DicoLine["FORMAT"] == "HYB"):
            LabelObj = A429LabelHYB(DicoLine["LABEL OUT"], DicoLine["SDI OUT"], DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],  DicoLine["RESOLUTION"])

        LabelObj.accuracy=DicoLine["FULL SCALE CODING ACCURACY"]

    # in case of DIS A429 label FORMAT field is empty
    else:
        LabelObj = A429LabelDIS(DicoLine["LABEL OUT"], DicoLine["SDI OUT"])

    LabelObj.input_trans_rate = DicoLine["OUTPUT TRANSMIT INTERVAL"]
    LabelObj.originATA = DicoLine["ORIGIN ATA"]
    LabelObj.pins = DicoLine["OUTPUT PINS"]
    LabelObj.source = DicoLine["SOURCE OR UPSTREAM COMPUTER NAME"]
    LabelObj.nature = DicoLine['NATURE']

    return LabelObj

def main():

    print(sys.argv[1])

    bds_file=BDS(sys.argv[1])
    bds_file.parse_BDS()

    print (bds_file.BDS)

main()