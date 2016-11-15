import re
import xlrd,xlwt
import os
from MICD.MICD import MICD

class Mexico_Init_File(MICD):

    """
    Class to parse and analyze mexico inits files
    Mexico init file is a specific type of MICD with only one tab: "FUN_OUT" and with a reduced number of column
    So this class is a child of MICD class
    """
    MICD.file_structure = {

        'Excel_sheets':
            {
                'FUN_OUT': (
                'Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format',
                'From', 'Min', 'Max', 'Default Value')
            },
        # tab to do the equivalence between col number and MICD_port object attributes
        # so used to configure MICD_port object
        'MICD_portObjectConfigurationOUT': [
            'name',
            'codingtype',
            'unit',
            'description',
            'convention',
            'dim1',
            'dim2',
            'comformat',
            'fromto',
            'min',
            'max',
            'initdefaultvalue'
        ]
    }
    def __init__(self, pathname,flagNewFile=False):

        MICD.__init__(self,pathname, None, None, flagNewFile)

    # we have to overload createemptyfile function because of the reduced number of sheet (only FUN_OUT)
    # in MEXICO init file
    def createemptyfile(self):

        self._Workbook = xlwt.Workbook()

        # create file structure
        for _sheet in sorted(self._SheetAndIndex):

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

        return
