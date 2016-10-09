import csv
from BDS import (BDS)
from A429 import (A429Label,A429ParamDIS,A429ParamBNR,A429ParamBCD,A429ParamOpaque)

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
                LabelObj = self.ParseLine(row)
                self.add_Label(LabelObj)

        finally:
            file.close()

    def parse_BDSDis(self):
        """
        Method to analyse BDS Discrete file for EIS
        """
        pass

    def ParseLine(self, DicoLine):

        LabelObj=None
        ParamObj=None

        LabelObj = A429Label(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["FORMAT_BLOC"], DicoLine["SENS"], DicoLine["NOM_SOUS_ENS"])
        LabelObj.input_trans_rate = DicoLine["FREQU_CONT"]
        LabelObj.source = DicoLine["NOM_SUPP"]

        if DicoLine['FORMAT_PARAM'] == "BNR":

            ParamObj = A429ParamBNR(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], self.ComputeResolutionBNR(DicoLine["TAILLE"],DicoLine["ECHEL"]))


        elif DicoLine['FORMAT_PARAM'] == "BCD":
            ParamObj = A429ParamBCD(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], self.ComputeResolutionBCD(DicoLine["TAILLE"],DicoLine["ECHEL"]))

        elif DicoLine['FORMAT_PARAM'] == "DW":
            ParamObj = A429ParamDIS(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number)
            ParamObj.BitNumber = DicoLine["POSITION"]
            ParamObj.state0 = DicoLine["ETAT0"]
            ParamObj.state1 = DicoLine["ETAT1"]

        elif DicoLine['FORMAT_PARAM'] == "ISO5":

            ParamObj = A429ParamOpaque(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],DicoLine["TAILLE"])

        else:
            #print ("[BDS_EIS][ParseLine] Type non reconnu: " + DicoLine['FORMAT_PARAM'])
            return LabelObj

        ParamObj.numbloc = DicoLine["NOM_BLOC"]
        ParamObj.libbloc = DicoLine["LIB_BLOC"]
        ParamObj.comments = DicoLine["LIB_PARAM"]
        ParamObj.parameter_def = DicoLine["NOM_TYPE"]
        ParamObj.unit = DicoLine["UNITE"]

        LabelObj.refParameter(ParamObj)
        return LabelObj



