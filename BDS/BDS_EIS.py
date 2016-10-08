import csv
import re
from A429 import (A429Label,A429ParamBNR,A429ParamBCD,A429ParamDIS,A429ParamOpaque)

class BDS_EIS:
    """
    Class to defined BDS data file
    """

    def __init__(self,A429File,DISFile):
        """
        Attributes are:
        _ path name of the file
        """
        self.A429File = A429File
        self.DISFile = DISFile
        self.BDS = dict()
        self.BDS['A429LabelsList'] = dict()
        self.BDS['DISLabelsList'] = dict()
        self.BDS['ParamList'] = ()
        self.BDS['sourceList'] = dict()

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

    def add_Label(self, LabelOject):

        # an label identifier is a tuple made of the following fields
        # self.nature, self.system, self.number, self.sdi,self.source
        labelIdentifier=LabelOject.createIndentifier()
        if(labelIdentifier not in self.BDS['A429LabelsList'].keys()):
            self.BDS['A429LabelsList'][labelIdentifier] = LabelOject

    def add_Parameter(self, ParamOject):
        self.BDS['ParamList'].append(ParamOject)

    def add_Source(self, source):
        if (source not in self.BDS['sourceList']):
            self.BDS['sourceList'][source] = source

    def get_SourceList(self, source):
            return self.BDS['sourceList'][source]

    def get_LabelObjList(self,**paramdict):
        # self.nature, self.system, self.number, self.sdi,self.source
        mylabellist=[]

        if 'nature' in paramdict:
            naturesearched=str(paramdict['nature'])
        else:
            naturesearched=".*"

        if 'system' in paramdict:
            systemsearched=str(paramdict['system'])
        else:
            systemsearched=".*"

        if 'number' in paramdict:
            numbersearched=str(paramdict['number'])
            print ("numbersearched: "+numbersearched)
        else:
            numbersearched=".*"

        if 'sdi' in paramdict:
            sdisearched=str(paramdict['sdi'])
        else:
            sdisearched=".*"

        if 'source' in paramdict:
            sourcesearched=str(paramdict['source'])
        else:
            sourcesearched=".*"

        natureregexp=re.compile(naturesearched)
        systemregexp=re.compile(systemsearched)
        numberregexp=re.compile(numbersearched)
        sdiregexp=re.compile(sdisearched)
        sourceregexp=re.compile(sourcesearched)

        for (nature, system, number, sdi, source) in self.BDS['A429LabelsList'].keys():
            if natureregexp.search(str(nature)):
                if systemregexp.search(str(system)):
                    if numberregexp.search(str(number)):
                        if sdiregexp.search(str(sdi)):
                            if sourceregexp.search(str(source)):
                                mylabellist.append(self.BDS['A429LabelsList'][(nature, system, number, sdi, source)])
        return mylabellist



    def ParseLine(self, DicoLine):

        LabelObj=None
        ParamObj=None

        LabelObj = A429Label(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["FORMAT_BLOC"], DicoLine["SENS"], DicoLine["NOM_SOUS_ENS"])
        LabelObj.input_trans_rate = DicoLine["FREQU_CONT"]
        LabelObj.source = DicoLine["NOM_SUPP"]

        if DicoLine['FORMAT_PARAM'] == "BNR":

            ParamObj = A429ParamBNR(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], ComputeResolutionBNR(DicoLine["TAILLE"],DicoLine["ECHEL"]))


        elif DicoLine['FORMAT_PARAM'] == "BCD":
            ParamObj = A429ParamBCD(DicoLine["NOM_PARAM"], DicoLine["SENS"], LabelObj.number, DicoLine["POSITION"],
                                    DicoLine["TAILLE"], DicoLine["ECHEL"], ComputeResolutionBCD(DicoLine["TAILLE"],DicoLine["ECHEL"]))

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



def ComputeResolutionBCD(nb_bits, range):

    max_encoding = 0.0
    n_digit = 0
    nombre_bits=int(nb_bits)

    while nombre_bits > 3:
        max_encoding = max_encoding + 9*10**n_digit
        nombre_bits -= 4
        n_digit += 1
    if nombre_bits == 3:
        max_encoding = max_encoding + 7*10**n_digit
    elif nombre_bits == 2:
        max_encoding = max_encoding + 3*10**n_digit
    elif nombre_bits == 1:
        max_encoding = max_encoding + 1*10**n_digit

    return float(range) / max_encoding


def ComputeResolutionBNR(nb_bits, range):

    nombre_bits=int(nb_bits)

    if nombre_bits > 0:
        resolution = float(range) / (2 ** nombre_bits)
    else:
        resolution = None

    return resolution