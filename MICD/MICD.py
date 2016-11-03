import pathlib
import re
from datetime import datetime
import xlrd, xlwt

class MICD:
    """
    Class to parse/create MICD
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200; align: horiz left;border: top thin, right thin, bottom thin, left thin;')
    xls_style_bold = xlwt.easyxf('font: name Arial, bold on, height 200; pattern: pattern solid, fore_color turquoise; border: top thin, right thin, bottom thin, left thin; align: horiz left;')

    file_structure = {
        'HEADER': ('Identifier', 'Value'),
        'SIM_CTRL_IN': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
        'SIM_CTRL_OUT': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
        'PROFILE': ('Name', 'Type', 'Dim1', 'Description'),
        'AIRCRAFT_ICD': ('ICD Version', 'ICD File Name', 'Cross Ref File Name'),
        'SIMULATION_LEVEL': ('Platform Code', 'Simulation Level[1]'),
        'FUN_IN': ('Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode', 'From'
                   , "Refresh\nRate", 'Min', 'Max', 'Enum', 'Consumed If', 'Aircraft Signal Name', "Interface\nLevel",
                   'Status (SSM/FS/Refresh)',"Simulation\nLevel[1]", 'Init Value', 'Custom', 'Comment'),
        'FUN_OUT': ('Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode',
                    'To', "Refresh\nRate",'Min', 'Max', 'Enum', 'Produced If', 'Aircraft Signal Name',"Interface\nLevel"
                    , 'Status (SSM/FS/Refresh)', "Simulation\nLevel[1]", 'Comment', 'Not Simulated Data',
                    'Default Value')
    }

    def __init__(self, pathname, modelname=None, modelversion=None, newfile=None):

        self._pathName = pathname
        self._modelName = modelname
        self._version = modelversion
        self._newFile = newfile
        self._Workbook = None
        self._SheetAndIndex = {}

        if self._newFile is True:

            for sheet in MICD.file_structure.keys():
                self._SheetAndIndex[sheet] = {}
                self._SheetAndIndex[sheet]['ColIndex'] = 0
                self._SheetAndIndex[sheet]['ColNbr'] = len(list(MICD.file_structure[sheet]))
                self._SheetAndIndex[sheet]['RowIndex'] = 0
                self._SheetAndIndex[sheet]['RowNbr'] = 0
                self._SheetAndIndex[sheet]['Header'] = list(MICD.file_structure[sheet])
                self._SheetAndIndex[sheet]['XlsSheet'] = None

            self.createemptyfile()
        else:
            self.parse()

    def parse(self):
        return


    # function to create a new MICD file
    def createemptyfile(self):

        self._Workbook = xlwt.Workbook()

        # create file structure
        for _sheet in self._SheetAndIndex:

            # add sheet in workbook
            self._SheetAndIndex[_sheet]['XlsSheet'] = self._Workbook.add_sheet(_sheet)

            # header creation
            for _header_cell in list(self._SheetAndIndex[_sheet]['Header']):

                self._SheetAndIndex[_sheet]['XlsSheet'].write(self._SheetAndIndex[_sheet]['RowIndex'],
                                                              self._SheetAndIndex[_sheet]['ColIndex'],
                                                              _header_cell,
                                                              MICD.xls_style_bold)
                self._SheetAndIndex[_sheet]['ColIndex'] += 1

            # update object information
            self._SheetAndIndex[_sheet]['ColIndex'] = 0
            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        # fill header sheet
        _sheet = 'HEADER'

        # date computation for information
        _date = datetime.now()
        _displaydate = str(_date.day)+"/"+str(_date.month)+"/"+str(_date.year)

        # create and temp dictonnary it will be used to fill header sheet in a loop
        _headerDict = {'MOD': self._modelName,
                       'VER': self._version,
                       'ORG': 'EYYSEV',
                       'DAT': _displaydate,
                       'ACI': '',
                       'APP': '',
                       'REF': '',
                       'VIT': '8.1'}
        # loop to write header cell
        for _ident, _value in _headerDict.items():

            self.writeCell(_sheet, 'Identifier', _ident,True)
            self.writeCell(_sheet, 'Value', _value)
            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        return



    def writeCell(self,sheet,field,value,title=None):

        if title is None:
            _styleToApply = MICD.xls_style
        elif title is True:
            _styleToApply = MICD.xls_style_bold
        else:
            _styleToApply = None
        _index = self.file_structure[sheet].index(field)


        self._SheetAndIndex[sheet]['XlsSheet'].write(self._SheetAndIndex[sheet]['RowIndex'],
                                                     _index,
                                                     value,
                                                     _styleToApply)
        self._SheetAndIndex[sheet]['ColIndex'] += 1


    # function to save current MICD object (pathname attribute
    # is used to save the file
    def savefile(self):
        """
        Method to save a BDS2XML tool input file from BDS2XML current object
        :return True/False:
        """
        self._Workbook.save(self._pathName)

