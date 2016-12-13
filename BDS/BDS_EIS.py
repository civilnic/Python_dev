import csv

from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque, A429ParamISO5)
from .BDS import (BDS)


class BDS_EIS(BDS):
    """
    Class to defined BDS data file
    """

    def __init__(self,A429File,DISFile):
        """
        Attributes are:
        _ path name of the file
        """
        super(BDS_EIS, self).__init__()
        self.A429File = A429File
        self.DISFile = DISFile

        self.parse_BDSA429()
        self.parse_BDSDis()

    def parse_BDSA429(self):
        """
        Method to analyse BDS A429 file for EIS
        For this file header is made of the following fields:
        NOM_LIAISON	NOM_SUPP	TYPE_SUPPORT	LIB_SUPP	VITES	SENS	NOM_SOUS_ENS	NOM_CONT	LIB_CONT
        TYPE_UTIL_CONT	FREQU_CONT	LABEL	SDI	NOM_BLOC	LIB_BLOC	FORMAT_BLOC	SSM_TYPE	NOM_PARAM	LIB_PARAM
        NOM_TYPE	FORMAT_PARAM	POSITION	TAILLE	SIGNE	ECHEL	DOMAINE_VALEUR	UNITE	ETAT0	ETAT1
        """
        file = open(self.A429File, "r")

        try:
            #
            # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
            #
            reader = csv.DictReader(file, delimiter=';')

            #
            # read data
            #
            for row in reader:
                self.ParseLine(row)
                #self.add_Label(LabelObj)

        finally:
            file.close()

    def parse_BDSDis(self):
        """
        Method to analyse BDS Discrete file for EIS
        """
        pass

    def ParseLine(self, DicoLine):

        LabelObj = A429Label(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["FORMAT_BLOC"], DicoLine["SENS"], DicoLine["NOM_SOUS_ENS"])
        LabelObj.input_trans_rate = DicoLine["FREQU_CONT"]
        LabelObj.source = DicoLine["NOM_SUPP"]

        LabelObj = self.add_Label(LabelObj)

        SetLabelFormattedName(LabelObj)

        if DicoLine['FORMAT_PARAM'] == "BNR":

            ParamObj = A429ParamBNR(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], self.ComputeResolutionBNR(DicoLine["TAILLE"],DicoLine["ECHEL"]))
            ParamObj.signed = DicoLine["SIGNE"]

        elif DicoLine['FORMAT_PARAM'] == "BCD":
            ParamObj = A429ParamBCD(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], self.ComputeResolutionBCD(DicoLine["TAILLE"],DicoLine["ECHEL"]))
            ParamObj.signed = DicoLine["SIGNE"]

        elif DicoLine['FORMAT_PARAM'] == "DW":
            ParamObj = A429ParamDIS(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number)
            ParamObj.BitNumber = DicoLine["POSITION"]
            ParamObj.state0 = DicoLine["ETAT0"]
            ParamObj.state1 = DicoLine["ETAT1"]


        elif DicoLine['FORMAT_PARAM'] == "ISO5":

            ParamObj = A429ParamISO5(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],DicoLine["TAILLE"])


        elif DicoLine['FORMAT_PARAM'] == "Opaque":

            ParamObj = A429ParamOpaque(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],DicoLine["TAILLE"])

        else:
            #print ("[BDS_EIS][ParseLine] Type non reconnu: " + DicoLine['FORMAT_PARAM'])
            return LabelObj

        ParamObj.formatparam = DicoLine['FORMAT_PARAM']
        ParamObj.nombloc = DicoLine["NOM_BLOC"]
        ParamObj.libbloc = DicoLine["LIB_BLOC"]
        ParamObj.comments = DicoLine["LIB_PARAM"]
        ParamObj.parameter_def = DicoLine["LIB_PARAM"]
        ParamObj.unit = DicoLine["UNITE"]

        LabelObj.refParameter(ParamObj)

        SetParameterPreFormattedName(ParamObj)

        return LabelObj

def SetLabelFormattedName(LabelObj):

    # set formatted name (i.e simulation label name)pip
    try:
        int(LabelObj.sdi, 2)
    except ValueError:
        _sdi = str(LabelObj.sdi)
        if (_sdi == "DD") or (_sdi == "XX"):
            _sdi = "x"

        LabelObj.SimuFormattedName = str(LabelObj.source) + "a4_w" + _sdi + str("%03d" % LabelObj.number)
    else:
        LabelObj.SimuFormattedName = str(LabelObj.source) + "a4_w" + str(int(LabelObj.sdi, 2)) + str("%03d" % LabelObj.number)

def SetParameterPreFormattedName(ParamObj):

    LabelObj=ParamObj.labelObj

    if LabelObj.labeltype == "DW":
        ParamObj.SimuPreFormattedName = str(LabelObj.source) + "_L" + str("%03d" % LabelObj.number) + "_B" + str(ParamObj.BitNumber) + "_" + str(ParamObj.name)
    else:
        ParamObj.SimuPreFormattedName = str(LabelObj.source) + "_L" + str("%03d" % LabelObj.number) + "_" + str(ParamObj.name)