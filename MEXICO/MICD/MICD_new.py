import pandas as pd



class MICD_new:
    """
    Class to parse/create MICD
    """

    def __init__(self, pathname):

        self._pathName = pathname
        self.parse()

    def parse(self):

        print("[MICD]{parse] Parse excel file: " + self._pathName)
        self._dataframe = pd.read_excel(self._pathName)

        print(self._dataframe.index)
        print(self._dataframe.columns)

        xl = pd.ExcelFile(self._pathName)
        print(xl.sheet_names)