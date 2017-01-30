import re
import copy

from lxml import etree

from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque)
from BDS.BDS import BDS


class BDS_FWC(BDS):
    """
    Class to defined BDS data file
    """
    ConnectorMap = dict()
    ConfigXMLPath = "/MSP_ATA31/FWC/connector_map/input"

    def __init__(self, pathname, connectormapfile):
        """
        Attributes are:
        _ path name of the file
        """
        super().__init__()


        self.PathName=pathname
        self.ConnectorMapFile = connectormapfile

        self.parseMapFile(self.ConfigXMLPath)
        self.parse_BDS()


    def parseMapFile(self, pathXML):
        """
        Method to parse connector map file (to create formatted label name of FWC)
        """
        print(self.ConnectorMapFile)
        if self.ConnectorMapFile:
            try:
                tree = etree.parse(self.ConnectorMapFile)
            except:
                print("Cannot open FWC connector map file: "+self.ConnectorMapFile)
                return None

        for input in tree.xpath(pathXML):

            connector = input.get("connector")

            if connector not in self.ConnectorMap.keys():
                print(connector)
                self.ConnectorMap[connector] = dict()
            print(input.get("id"))
            self.ConnectorMap[connector]["type"] = input.get("type")
            self.ConnectorMap[connector]["source"] = input.get("source")
            self.ConnectorMap[connector]["id"] = input.get("id")

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

        # specific case of SDAC source:
        # contrarily of other systems as EIU1 and EIU2 that have one line per label/parameters from each
        # SDAC 1 and 2 labels/parameters are not distinguished (there is only one line for both of them)
        #  "INPUT PINS" field is equal to LMP04J,K,RMP04A,B for SDAC1/2
        # in this case for each label that "INPUT PINS" field is equal to LMP04J,K,RMP04A,B
        # we have to duplicate it into 2 labels/parameters one from SDAC1 pins=LMP04J,K one from SDAC2 pins=RMP04A,B
        # we create here BDSFILE_NEW_LIST line list with duplicated line for SDAC1 and SDAC2

        BDSFILE_NEW_LIST=[]
        for line in BDSFILE_LIST:
            _m = re.match(r'(.{66})(\w{6},\w),(\w{6},\w)(.*?)SDAC1/2(.*)', line)
            if _m:
                _newLine1=_m.group(1)+_m.group(2)+' '*9+_m.group(4)+'SDAC1'+' '*2+_m.group(5)
                _newLine2=_m.group(1)+_m.group(3)+' '*9+_m.group(4)+'SDAC2'+' '*2+_m.group(5)
                BDSFILE_NEW_LIST.append(_newLine1)
                BDSFILE_NEW_LIST.append(_newLine2)
            else:
                BDSFILE_NEW_LIST.append(line)



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
        for line in BDSFILE_NEW_LIST:

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
                DicoLine[field] = line[BDS_Parameters[field][0]:BDS_Parameters[field][1]].strip()

            # nature of data on current line "ENTREE"/"SORTIE"/"E/S"
            nature = DicoLine['NATURE']

            # input / output type
            typeIO = DicoLine['TYPE NAME']

            # in case of A429 data, I/O type is "NUM" or "BOOLEAN"
            if(typeIO == "NUM") or (typeIO == "BOOLEAN"):

                if(nature == "ENTREE"):
                    LabelObj = self.AddInputLabel(DicoLine)
                    LabelObj = self.add_Label(LabelObj)

                    # add associate parameter
                    ParamObj = self.AddParameter(DicoLine, LabelObj)
                    self.add_Parameter(ParamObj)

                elif (nature == "SORTIE"):
                    LabelObj = self.AddOutputLabel(DicoLine)
                    LabelObj = self.add_Label(LabelObj)

                    # add associate parameter
                    ParamObj= self.AddParameter(DicoLine, LabelObj)
                    self.add_Parameter(ParamObj)

                elif (nature == "E/S"):
                    #
                    # for E/S label we have to create on label on input and one label on output
                    # output label are link to input label with attribute LinkToInput = label input number
                    #
                    # add input label
                    LabelObj = self.AddInputLabel(DicoLine)
                    LabelObj.nature = "ENTREE"
                    labelnum = LabelObj.number
                    LabelObj = self.add_Label(LabelObj)

                    # add associate parameter
                    DicoLine["NATURE"] = "ENTREE"   # force nature field to "SORTIE" for param object creation
                                                    # only ENTREE or SORTIE values for nature
                                                    #  are possible for parameter creation
                    ParamObj = self.AddParameter(DicoLine, LabelObj)
                    self.add_Parameter(ParamObj)

                    # add output label
                    LabelObj = self.AddOutputLabel(DicoLine)
                    LabelObj.nature = "SORTIE"
                    LabelObj.LinkToInput = labelnum
                    LabelObj = self.add_Label(LabelObj)

                    # add associate parameter
                    DicoLine["NATURE"] = "SORTIE"   # force nature field to "ENTREE" for param object creation
                                                    # only ENTREE or SORTIE values for nature
                                                    #  are possible for parameter creation
                    ParamObj = self.AddParameter(DicoLine, LabelObj)
                    self.add_Parameter(ParamObj)
                #else:
                    #print("Label nature not defined:"+nature)

            # case of SYNCHRO label .i.e label in FWC input transmitted without modification on FWC output (same label
            # number and characteristisc

            elif(typeIO == "SYNCHRO"):

                if (nature == "E/S"):

                    # we suppose here that only output label information (number, sdi ...) are filled
                    # we create first an output label number and copy it as an input label

                    # add associate parameter
                    DicoLine["NATURE"] = "SORTIE"   # force nature field to "SORTIE" for param object creation
                                                    # only ENTREE or SORTIE values for nature
                                                    #  are possible for parameter creation

                    # add output label
                    LabelObj = self.AddOutputLabel(DicoLine)
                    LabelObj.nature = "SORTIE"
                    # weird things on BDS
                    # only inputs pins are filled for SYNCHRO label despite all other label informations are set
                    # by output fields
                    LabelObj.pins = DicoLine["INPUT PINS"]
                    LabelObj.LinkToInput = LabelObj.number
                    # to update formmatted name
                    self.SetLabelFormattedName(LabelObj)
                    LabelObj = self.add_Label(LabelObj)


                    ParamObj = self.AddParameter(DicoLine, LabelObj)
                    self.add_Parameter(ParamObj)



                    # create here the same label in input
                    _LabelObjIN = copy.copy(LabelObj)

                    # add new input label
                    _LabelObjIN.nature = "ENTREE"
                    _LabelObjIN = self.add_Label(_LabelObjIN)
                    # to update formmatted name
                    self.SetLabelFormattedName(LabelObj)
                    # add associate parameter
                    DicoLine["NATURE"] = "ENTREE"   # force nature field to "ENTREE" for param object creation
                                                    # only ENTREE or SORTIE values for nature
                                                    #  are possible for parameter creation
                    ParamObj = self.AddParameter(DicoLine, _LabelObjIN)
                    self.add_Parameter(ParamObj)


                # this case is not possible due to label SYNCHRO nature
                else:
                    pass
            # case of discrete data
            elif(typeIO == "DISCRET"):
                pass
            # other I/O type
            else:
                pass
            #TODO: Discret and other than A429 data type treatment

    def AddParameter(self, DicoLine, LabelObj):

        ParamObj=None

        # in FWC BDS msb is not specified
        # we assume that msb = 28 for BNR and 29 for BCD
        msb_bnr = 28
        msb_bcd = 29

        if DicoLine["FORMAT"]:
            if DicoLine["FORMAT"] == "BNR":
                ParamObj = A429ParamBNR(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number, msb_bnr, DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"], self.ComputeResolutionBNR(DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"]))
                ParamObj.accuracy = DicoLine["FULL SCALE CODING ACCURACY"]
                ParamObj.signed = True
            elif DicoLine["FORMAT"] == "HYB":
                if LabelObj.labeltype:
                    LabelObj.labeltype = "HYB"
                if DicoLine["TYPE NAME"] == "NUM":
                    if DicoLine["RANGE MAX"] =="" or DicoLine["RESOLUTION"] =="":
                        ParamObj = A429ParamOpaque(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number,
                                                   msb_bcd, DicoLine["SIGNIFICANTS BITS"])
                    else:
                        ParamObj = A429ParamBNR(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number, msb_bnr,
                                            DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"],
                                            self.ComputeResolutionBNR(DicoLine["SIGNIFICANTS BITS"],
                                                                      DicoLine["RANGE MAX"]))
                    ParamObj.accuracy = DicoLine["FULL SCALE CODING ACCURACY"]
                    ParamObj.signed = True
                elif DicoLine["TYPE NAME"] == "BOOLEAN":
                    ParamObj = A429ParamDIS(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number)

                    if LabelObj.nature == "IN":
                        ParamObj.BitNumber = DicoLine["BIT IN"]
                        ParamObj.state0 = DicoLine["STATE 0 PARAMETER DEFINITION"]
                        ParamObj.state1 = DicoLine["STATE 1 PARAMETER DEFINITION"]
                    elif LabelObj.nature == "OUT":
                        ParamObj.BitNumber = DicoLine["BIT OUT"]
                        ParamObj.state0 = DicoLine["STATE 0 PARAMETER DEFINITION OUT"]
                        ParamObj.state1 = DicoLine["STATE 1 PARAMETER DEFINITION OUT"]
                else:
                    ParamObj = A429ParamOpaque(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number, msb_bcd, DicoLine["SIGNIFICANTS BITS"])
            elif DicoLine["FORMAT"] == "BCD":
                ParamObj = A429ParamBCD(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number, msb_bcd, DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"], self.ComputeResolutionBCD(DicoLine["SIGNIFICANTS BITS"], DicoLine["RANGE MAX"]))
            else:
                # TODO: Opaque and ISO5 labels are not treated yet in BDS_FWC
                # Opaque and ISO5 format are not treated yet
                print("[BDS_FWC: Label format not treated" + str(DicoLine["FORMAT"]))
        # in case of DIS A429 Parameter FORMAT field is empty
        else:
            ParamObj = A429ParamDIS(DicoLine["IDENTIFICATOR"], DicoLine["NATURE"], LabelObj.number)

            if LabelObj.nature == "IN":
                ParamObj.BitNumber = DicoLine["BIT IN"]
                ParamObj.state0 = DicoLine["STATE 0 PARAMETER DEFINITION"]
                ParamObj.state1 = DicoLine["STATE 1 PARAMETER DEFINITION"]
            elif LabelObj.nature == "OUT":
                ParamObj.BitNumber = DicoLine["BIT OUT"]
                ParamObj.state0 = DicoLine["STATE 0 PARAMETER DEFINITION OUT"]
                ParamObj.state1 = DicoLine["STATE 1 PARAMETER DEFINITION OUT"]

        ParamObj.comments = DicoLine["COMMENTS"]
        ParamObj.parameter_def = DicoLine["PARAMETER DEFINITION"]
        ParamObj.unit = DicoLine["UNIT"]

        LabelObj.refParameter(ParamObj)

        self.SetParameterPreFormattedName(ParamObj)

        return ParamObj


    def AddInputLabel(self, DicoLine):

        # label format is set with FORMAT field if not empty
        if DicoLine["FORMAT"]:
            label_format = DicoLine["FORMAT"]
        # else in FWC BDS file an empty FORMAT is considered as a DW (Discrete Word) label
        else:
            label_format = "DW"

        LabelObj = A429Label(DicoLine["LABEL IN"], DicoLine["SDI IN"], label_format, DicoLine["NATURE"], DicoLine["SYSTEM"])
        LabelObj.input_trans_rate = DicoLine["INPUT TRANSMIT INTERVAL MIN/MAX"]
        LabelObj.originATA = DicoLine["ORIGIN ATA"]
        LabelObj.pins = DicoLine["INPUT PINS"]
        LabelObj.source = DicoLine["SOURCE OR UPSTREAM COMPUTER NAME"].replace("/", "_")

        LabelObj.source = re.sub(r'\.', '_',  LabelObj.source)

        self.SetLabelFormattedName(LabelObj)

        return LabelObj

    def AddOutputLabel(self, DicoLine):

        # label format is set with FORMAT field if not empty
        if DicoLine["FORMAT"]:
            label_format = DicoLine["FORMAT"]
            # in FWC BDS file an empty FORMAT is considered as a DW (Discrete Word) label
        else:
            label_format = "DW"

        LabelObj = A429Label(DicoLine["LABEL OUT"], DicoLine["SDI OUT"], label_format, DicoLine["NATURE"], DicoLine["SYSTEM"])
        LabelObj.input_trans_rate = DicoLine["OUTPUT TRANSMIT INTERVAL"]
        LabelObj.originATA = DicoLine["ORIGIN ATA"]
        LabelObj.pins = DicoLine["OUTPUT PINS"]

        LabelObj.source = DicoLine["SOURCE OR UPSTREAM COMPUTER NAME"].replace("/", "_")

        LabelObj.source = re.sub(r'\.', '_',  LabelObj.source)

        self.SetLabelFormattedName(LabelObj)

        return LabelObj



    def SetLabelFormattedName(self, LabelObj):

        # set formatted name (i.e simulation label name)
        if LabelObj.pins in self.ConnectorMap.keys():
            connectorId = self.ConnectorMap[LabelObj.pins]['id']
        else:
            connectorId = ""

        _sdi = LabelObj.sdi
        if _sdi == "DD":
            _sdi = "D"
            LabelObj.SimuFormattedName = "E_" + connectorId + "_" + str("%03d" % LabelObj.number) + "_" + _sdi + "_1"
        elif _sdi == "XX":
            _sdi = "X"
            LabelObj.SimuFormattedName = "E_" + connectorId + "_" + str("%03d" % LabelObj.number) + "_" + _sdi + "_1"
        else:
            LabelObj.SimuFormattedName = "E_" + connectorId + "_" + str("%03d" % LabelObj.number) \
                                         + "_" + str(int(LabelObj.sdi, 2)) + "_1"

    def SetParameterPreFormattedName(self, ParamObj):

        LabelObj = ParamObj.labelObj
        parametername = str(ParamObj.name).replace(".", "_")

        if isinstance(ParamObj, A429ParamDIS):
            ParamObj.SimuPreFormattedName = str(LabelObj.source) + "_L" + str("%03d" % LabelObj.number) \
                                            + "_B" + str(ParamObj.BitNumber) + "_" + parametername
        else:
            ParamObj.SimuPreFormattedName = str(LabelObj.source) + "_L" + str("%03d" % LabelObj.number) + "_" + parametername

        ParamObj.SimuPreFormattedName = ParamObj.SimuPreFormattedName.replace(" ", "_")