import re
from A429 import (A429LabelBNR,A429LabelBCD,A429LabelHYB,A429LabelDIS,A429SignalBool,A429SignalFloat)
from BDS2XML import (BDS2XML)

class BDS_FWC:
    """
    Class to defined BDS data file
    """

    def __init__(self, path_name):
        """
        Attributes are:
        _ path name of the file
        """
        self.PathName = path_name
        self.BDS = dict()

        self.parse_BDS()

    def add_system(self,system):
        if system not in self.BDS.keys():
            self.BDS[system] = dict()
            self.BDS[system]['A429LabelsList'] = dict()
            self.BDS[system]['DISLabelsList'] = dict()
            self.BDS[system]['SignalList'] = dict()

    def add_Label(self,system,LabelNumber,LabelOject):
        self.BDS[system]['A429LabelsList'][LabelNumber]=LabelOject

    def get_LabelObj(self,system,LabelNumber):
        if LabelNumber in self.BDS[system]['A429LabelsList'].keys():
            return self.BDS[system]['A429LabelsList'][LabelNumber]
        else:
            return None

    def add_Signal(self,system,SignalName,SignalObj):
        self.BDS[system]['SignalList'][SignalName]=SignalObj

    def get_SignalObj(self, system, SignalName):
        if SignalName in self.BDS[system]['SignalList'].keys():
            return self.BDS[system]['SignalList'][SignalName]
        else:
            return None

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
            BDSFILE = open(self.PathName,'r')

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
            'STATE 1 PARAMETER DEFINITION':(295,335),
            'STATE 0 PARAMETER DEFINITION':(335,387),
            'STATE 1 PARAMETER DEFINITION OUT': (417, 457),
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


        #
        # analyzes each line of BDS files
        # each line is a string of approximately 618 bytes described upper by dictionary bds_complete_map
        # some fields of the line are unused that why we defined BDS_Parameters dictionary, it contains used field
        # to extract
        #
        for line in BDSFILE_LIST:

            # if empty line go to next line
            if not line:
                continue
            #
            # declare a new empty dictionary for line content
            # DicoLine will contain DicoLine['field']=field_value (extract from current line
            #
            DicoLine = dict()

            # declare objects
            LabelObj = None

            # split the line following BDS_parameters
            for field in BDS_Parameters.keys():
                DicoLine[field]=line[BDS_Parameters[field][0]:BDS_Parameters[field][1]].strip()

            # get current system
            system=DicoLine['SYSTEM']
            # add it to current BDS object
            self.add_system(system)

            # nature of data on current line "ENTREE"/"SORTIE"/"E/S"
            nature=DicoLine['NATURE']

            # input / output type
            typeIO=DicoLine['TYPE NAME']

            # in case of A429 data, I/O type is "NUM" or "BOOLEAN"
            if(typeIO=="NUM") or (typeIO=="BOOLEAN"):

                if(nature == "ENTREE"):
                    LabelObj = AddInputLabel(DicoLine)
                    self.add_Label(system,LabelObj.number,LabelObj)

                    # add associate signal
                    SignalObj= AddSignal(DicoLine,LabelObj)
                    self.add_Signal(system,SignalObj.name,SignalObj)

                elif (nature == "SORTIE"):
                    LabelObj = AddOutputLabel(DicoLine)
                    self.add_Label(system,LabelObj.number, LabelObj)

                    # add associate signal
                    SignalObj= AddSignal(DicoLine,LabelObj)
                    self.add_Signal(system,SignalObj.name,SignalObj)

                elif (nature == "E/S"):
                    #
                    # for E/S label we have to create on label on input and one label on output
                    # output label are link to input label with attribute LinkToInput = label input number
                    #
                    # add input label
                    LabelObj = AddInputLabel(DicoLine)
                    LabelObj.nature = "ENTREE"
                    labelnum = LabelObj.number
                    self.add_Label(system, LabelObj.number, LabelObj)

                    # add associate signal
                    SignalObj= AddSignal(DicoLine,LabelObj)
                    self.add_Signal(system,SignalObj.name,SignalObj)

                    # add output label
                    LabelObj = AddOutputLabel(DicoLine)
                    LabelObj.nature = "SORTIE"
                    LabelObj.LinkToInput=labelnum
                    self.add_Label(system, LabelObj.number, LabelObj)

                    # add associate signal
                    SignalObj= AddSignal(DicoLine,LabelObj)
                    self.add_Signal(system,SignalObj.name,SignalObj)
                #else:
                    #print("Label nature not defined:"+nature)

            # case of discrete data
            elif(typeIO=="DISCRET"):
                pass
            # other I/O type
            else:
                pass
            #TODO: Discret and other than A419 data type treatment

def AddSignal(DicoLine,LabelObj):

    SignalObj=None

    if(LabelObj.type=="BNR" or LabelObj.type=="HYB" or LabelObj.type=="BCD"):
        SignalObj = A429SignalFloat(DicoLine["IDENTIFICATOR"], LabelObj.nature, LabelObj.number)
    if(LabelObj.type == "DIS"):
        SignalObj = A429SignalBool(DicoLine["IDENTIFICATOR"], LabelObj.nature, LabelObj.number)

        if(LabelObj.nature=="ENTREE"):
            SignalObj.BitNumber=DicoLine["BIT IN"]
            SignalObj.state0=DicoLine["STATE 0 PARAMETER DEFINITION"]
            SignalObj.state1=DicoLine["STATE 1 PARAMETER DEFINITION"]
        elif(LabelObj.nature=="SORTIE"):
            SignalObj.BitNumber = DicoLine["BIT OUT"]
            SignalObj.state0 = DicoLine["STATE 0 PARAMETER DEFINITION OUT"]
            SignalObj.state1 = DicoLine["STATE 1 PARAMETER DEFINITION OUT"]

    SignalObj.comments=DicoLine["COMMENTS"]
    SignalObj.parameter_def=DicoLine["PARAMETER DEFINITION"]
    SignalObj.unit=DicoLine["UNIT"]

    LabelObj.addSignal(SignalObj)

    return SignalObj



def AddInputLabel(DicoLine):

    LabelObj=None


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




