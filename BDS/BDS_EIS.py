import csv


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
        self.BDS['SignalList'] = dict()

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
            reader = csv.DictReader(file,delimiter=';')

            #
            # read data
            #
            for row in reader:
                AddLabel(row)
        finally:
            file.close()

    def parse_BDSDis(self):
        """
        Method to analyse BDS Discrete file for EIS
        """
        pass

    def AddLabel(DicoLine):
        LabelObj = None

        if (DicoLine["FORMAT_BLOC"]):
            if (DicoLine["FORMAT_BLOC"] == "BNR"):

                LabelObj = A429LabelBNR(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["POSITION"],
                                        DicoLine["ECHEL"], ComputeResolutionBNR(DicoLine["TAILLE"],DicoLine["ECHEL"]))

            if (DicoLine["FORMAT_BLOC"] == "BCD"):

                LabelObj = A429LabelBCD(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["POSITION"],
                                        DicoLine["ECHEL"], ComputeResolutionBCD(DicoLine["TAILLE"],DicoLine["ECHEL"]))

            if (DicoLine["FORMAT_BLOC"] == "HYB"):
                LabelObj = A429LabelHYB(DicoLine["LABEL"], DicoLine["SDI"], DicoLine["POSITION"],
                                        DicoLine["ECHEL"], DicoLine["RESOLUTION"])


        # in case of DIS A429 label FORMAT field is empty
        elif (DicoLine["FORMAT_BLOC"] == "DW"):
            LabelObj = A429LabelDIS(DicoLine["LABEL"], DicoLine["SDI"])

        LabelObj.input_trans_rate = DicoLine["INPUT TRANSMIT INTERVAL MIN/MAX"]
        LabelObj.originATA = DicoLine["ORIGIN ATA"]
        LabelObj.pins = DicoLine["INPUT PINS"]
        LabelObj.source = DicoLine["SOURCE OR UPSTREAM COMPUTER NAME"]
        LabelObj.nature = DicoLine['NATURE']

        return LabelObj



    def ComputeResolutionBCD(nb_bits,range):

        max_encoding=0
        n_digit=0

        while nb_bits > 3:
            max_encoding = max_encoding + 9*10**n_digit
            nb_bits -= 4
            n_digit += 1
        if nb_bits==3:
            max_encoding = max_encoding + 7*10**n_digit
        elif nb_bits==2:
            max_encoding = max_encoding + 3*10**n_digit
        elif nb_bits==1:
            max_encoding = max_encoding + 1*10**n_digit

        return range / max_encoding


    def ComputeResolutionBNR(nb_bits,range):

        if nb_bits > 0:
            resolution = range / (2 ** nb_bits)
        else
            resolution = None

        return resolution