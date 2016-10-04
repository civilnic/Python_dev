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
        """
        file = open(self.A429File, "r")

        try:
            #
            # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
            #
            reader = csv.DictReader(file,delimiter=';')

            #
            # print read data
            #
            for row in reader:
                print (row)
        finally:
            file.close()

    def parse_BDSDis(self):
        """
        Method to analyse BDS Discrete file for EIS
        """
        pass