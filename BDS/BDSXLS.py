import xlwt
import xlrd
from re import match
from BDS.BDS import BDS
from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque)

class BDSXLS(BDS):
    """
    Class to defined BDSXLS input data file
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200;')

    file_structure = {
        'IN': ['A429 Label Name','From','Port Name','Type','Label Number','SDI','Label type','Ssm Type','Parameter Name','Parameter Format','Description','Unit','Parameter MSB','Size','Signed','Range','Bool False Def','Bool True Def','Comments'],
        'OUT': ['A429 Label Name','From','Port Name','Type','Label Number','SDI','Label type','Ssm Type','Parameter Name','Parameter Format','Description','Unit','Parameter MSB','Size','Signed','Range','Bool False Def','Bool True Def','Comments']
    }

    def __init__(self, path_name , new):
        """
        Attributes are:
        _ path name of the file
        """
        self.PathName = path_name
        self.Workbook = None
        self.SheetAndIndex = {}

        # heritage of BDS class
        super().__init__()

        if new is True:
            for sheet in BDSXLS.file_structure.keys():
                self.SheetAndIndex[sheet]={}
                self.SheetAndIndex[sheet]['ColIndex'] = 0
                self.SheetAndIndex[sheet]['ColNbr'] = len(list(BDSXLS.file_structure[sheet]))
                self.SheetAndIndex[sheet]['RowIndex'] = 0
                self.SheetAndIndex[sheet]['RowNbr'] = 0
                self.SheetAndIndex[sheet]['Header'] = list(BDSXLS.file_structure[sheet])
                self.SheetAndIndex[sheet]['XlsSheet'] = None

            self.createemptyfile()

        # open an existing file
        else:

            self._Workbook = xlrd.open_workbook(self.PathName)

            for _sheetname in self._Workbook.sheet_names():

                _testOnSheetNameFUNIN = match(r'IN', _sheetname)
                _testOnSheetNameFUNOUT = match(r'OUT', _sheetname)

                # sheet name match *_IN => it's a FUN_IN sheet name
                # this test is usefull in case of multiple input port sheets
                if _testOnSheetNameFUNIN:
                    _sheet = "FUN_IN"
                    _portType = "IN"

                elif _testOnSheetNameFUNOUT:
                    _sheet = "FUN_OUT"
                    _portType = "OUT"

                else:
                    continue

                _sheet = self._Workbook.sheet_by_name(_sheetname)

                self.SheetAndIndex[_sheetname] = {}
                self.SheetAndIndex[_sheetname]['ColIndex'] = 0
                self.SheetAndIndex[_sheetname]['ColNbr'] = _sheet.ncols
                self.SheetAndIndex[_sheetname]['RowIndex'] = 0
                self.SheetAndIndex[_sheetname]['RowNbr'] = _sheet.nrows
                self.SheetAndIndex[_sheetname]['Header'] = _sheet.row_values(0)
                self.SheetAndIndex[_sheetname]['XlsSheet'] = None

                for _rowidx in range(1, _sheet.nrows):  # Iterate through rows

                    for _indice,_field in enumerate(BDSXLS.file_structure[_sheet]): # iterate through columns



                    _line = _sheet.row_values(_rowidx)




            #TODO: initialisation de la classe BDSXLS sur un fichier existant: parsing et initialisation des index

    def __del__(self):
        self.savefile()

    def createemptyfile(self):
        """
        Method to create an empty BDSXLS input file
        :return True/False:
        """
        self.Workbook = xlwt.Workbook()

        for sheet in self.SheetAndIndex:

            # add sheet in workbook
            self.SheetAndIndex[sheet]['XlsSheet'] = self.Workbook.add_sheet(sheet)

            # header creation
            for header_cell in list(self.SheetAndIndex[sheet]['Header']):
                self.SheetAndIndex[sheet]['XlsSheet'].write(self.SheetAndIndex[sheet]['RowIndex'], self.SheetAndIndex[sheet]['ColIndex'], header_cell, BDSXLS.xls_style)
                self.SheetAndIndex[sheet]['ColIndex'] += 1

            # update object information
            self.SheetAndIndex[sheet]['ColIndex'] = 0
            self.SheetAndIndex[sheet]['RowIndex'] += 1
            self.SheetAndIndex[sheet]['RowNbr'] += 1

    def AddLine(self, ParameterObj):

        linedict = dict()

        # wich tab must be filled with parameter values
        LabelObj = ParameterObj.labelObj

        if LabelObj.nature == "IN":
            sheet = "IN"
        elif LabelObj.nature == "OUT":
            sheet = "OUT"
        else:
            print("Unknwon label nature: " + LabelObj.nature)

        self.fillLineDict(ParameterObj, linedict)


        for field in linedict.keys():
            self.writeCell(sheet, field, linedict[field])

        self.SheetAndIndex[sheet]['ColIndex'] = 0
        self.SheetAndIndex[sheet]['RowIndex'] += 1

    def writeCell(self, sheet, field, value):

        index = self.file_structure[sheet].index(str(field))

        self.SheetAndIndex[sheet]['XlsSheet'].write(self.SheetAndIndex[sheet]['RowIndex'],
                                                    index,
                                                    value,
                                                    BDSXLS.xls_style
                                                    )
        self.SheetAndIndex[sheet]['ColIndex'] += 1


    def savefile(self):
        """
        Method to save a BDSXLS tool input file from BDSXLS current object
        :return True/False:
        """
        self.Workbook.save(self.PathName)


    def fillLineDict(self, ParameterObj, linedict):

        LabelObj=ParameterObj.labelObj

        # 'From'
        linedict['From'] = LabelObj.source

        # 'Name PF',
        linedict['Port Name'] = ParameterObj.SimuPreFormattedName

        # 'Type'
        linedict['Type'] = ParameterObj.codingtype

        # 'Name F'
        linedict['A429 Label Name'] = LabelObj.SimuFormattedName

        # 'Label Number'
        linedict['Label Number'] = str(LabelObj.number)

        # 'SDI'
        linedict['SDI'] = str(LabelObj.sdi)

        # 'NOM_BLOC'
        linedict['Label type'] = LabelObj.labeltype

        # 'SSM_TYPE'
        linedict['Ssm Type'] = LabelObj.ssmtype

        # 'NOM_PARAM'
        linedict['Parameter Name'] = ParameterObj.name

        # 'FORMAT_PARAM'
        if ParameterObj.formatparam:
            linedict['Parameter Format'] = ParameterObj.formatparam
        else:
            linedict['Parameter Format'] = LabelObj.labeltype

        # 'LIB_PARAM'
        linedict['Description'] = ParameterObj.parameter_def

        # 'UNIT'
        linedict['Unit'] = ParameterObj.unit

        if isinstance(ParameterObj, A429ParamDIS):

            # 'ETAT_0'
            linedict['Bool False Def'] = ParameterObj.state0
            # 'ETAT_1'
            linedict['Bool True Def'] = ParameterObj.state1

            # 'TAIL'
            linedict['Size'] = 1

            # 'POSI'
            linedict['Parameter MSB'] = ParameterObj.BitNumber

        elif isinstance(ParameterObj, A429ParamBNR) or isinstance(ParameterObj, A429ParamBCD):

            # 'TAIL'
            linedict['Size'] = ParameterObj.nb_bits

            # 'POSI'
            linedict['Parameter MSB'] = ParameterObj.msb

            # 'SGN'
            linedict['Signed'] = ParameterObj.signed

            # 'ECHEL'
            linedict['Range'] = ParameterObj.range
