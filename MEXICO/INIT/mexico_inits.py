import re
import xlrd
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
        print(MICD)
        MICD.__init__(self,pathname, None, None, flagNewFile)
