import pathlib
import re
import xlrd, xlwt

class MICD:
    """
    Class to parse/create MICD
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200;')

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

    def __init__(self, pathname, modelname=None, newfile=None):

        self._pathName = pathname
        self._modelName = modelname
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

        for sheet in self._SheetAndIndex:

            # add sheet in workbook
            self._SheetAndIndex[sheet]['XlsSheet'] = self._Workbook.add_sheet(sheet)

            # header creation
            for header_cell in list(self._SheetAndIndex[sheet]['Header']):
                self._SheetAndIndex[sheet]['XlsSheet'].write(self._SheetAndIndex[sheet]['RowIndex'],
                                                             self._SheetAndIndex[sheet]['ColIndex'],
                                                             header_cell, MICD.xls_style)
                self._SheetAndIndex[sheet]['ColIndex'] += 1

            # update object information
            self._SheetAndIndex[sheet]['ColIndex'] = 0
            self._SheetAndIndex[sheet]['RowIndex'] += 1
            self._SheetAndIndex[sheet]['RowNbr'] += 1





        return

    def writeCell(self, sheet, field, value):

        index = self.file_structure[sheet].index(field)

        self._SheetAndIndex[sheet]['XlsSheet'].write(self._SheetAndIndex[sheet]['RowIndex'],
                                                    index,
                                                    value,
                                                    MICD.xls_style
                                                    )
        self._SheetAndIndex[sheet]['ColIndex'] += 1



    # function to save current MICD object (pathname attribute
    # is used to save the file
    def save(self):
        return

