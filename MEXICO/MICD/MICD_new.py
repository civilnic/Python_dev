import pandas as pd
from datetime import datetime
# from xltable import CellStyle,Table,Workbook,Worksheet

class MICD_new:
    """
    Class to parse/create MICD
    """
    file_structure = {

        'Excel_sheets':
            {
                'HEADER': ('Identifier', 'Value'),
                'SIM_CTRL_IN': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
                'SIM_CTRL_OUT': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
                'PROFILE': ('Name', 'Type', 'Dim1', 'Description'),
                'AIRCRAFT_ICD': ('ICD Version', 'ICD File Name', 'Cross Ref File Name'),
                'SIMULATION_LEVEL': ('Platform Code', 'Simulation Level[1]'),
                'FUN_IN': (
                'Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode', 'From'
                , "Refresh\nRate", 'Min', 'Max', 'Enum', 'Consumed If', 'Aircraft Signal Name', "Interface\nLevel",
                'Status (SSM/FS/Refresh)', "Simulation\nLevel[1]", 'Init Value', 'Custom', 'Comment',
                'Last Modification'),
                'FUN_OUT': (
                'Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode',
                'To', "Refresh\nRate", 'Min', 'Max', 'Enum', 'Produced If', 'Aircraft Signal Name'
                , "Interface\nLevel", 'Status (SSM/FS/Refresh)', "Simulation\nLevel[1]", 'Comment',
                'Not Simulated Data', 'Default Value', 'Last Modification')
            },
        # tab to do the equivalence between col number and MICD_port object attributes
        # so used to configure MICD_port object
        'MICD_portObjectConfigurationIN': [
            'name',
            'codingtype',
            'unit',
            'description',
            'convention',
            'dim1',
            'dim2',
            'comformat',
            'commode',
            'fromto',
            'resfreshrate',
            'min',
            'max',
            'enum',
            'prodconsif',
            'aircraftsignalname',
            'interfacelevel',
            'status',
            'simulationlevel',
            'initdefaultvalue',
            'notsimudatacustom',
            'comment',
            'lastmodification'
        ],
        'MICD_portObjectConfigurationOUT': [
            'name',
            'codingtype',
            'unit',
            'description',
            'convention',
            'dim1',
            'dim2',
            'comformat',
            'commode',
            'fromto',
            'resfreshrate',
            'min',
            'max',
            'enum',
            'prodconsif',
            'aircraftsignalname',
            'interfacelevel',
            'status',
            'simulationlevel',
            'comment',
            'notsimudatacustom',
            'initdefaultvalue',
            'lastmodification'
        ]
    }


    def __init__(self, pathname, modelname=None, modelversion=None, newfile=False):

        self._pathName = pathname
        self._modelName = modelname
        self._version = modelversion
        self._newFile = newfile
        self._Workbook = None
        self._Ports = {}
        self._ACICD = {}
        self._SheetAndIndex = {}

        if self._newFile is True:

            for _sheet in MICD_new.file_structure['Excel_sheets'].keys():
                pass

            self.createemptyfile()
        else:
            self.parse()

    def createemptyfile(self):

        # date computation for information
        _date = datetime.now()
        _displaydate = str(_date.day)+"/"+str(_date.month)+"/"+str(_date.year)

        # Create a Pandas dataframe from some data.
        _header_df = pd.DataFrame({'Identifier': ['ACI', 'APP', 'DAT', 'MOD', 'ORG', 'REF', 'VER', 'VIT'],
                                   'Value': ['','',_displaydate,self._modelName,'EYYSEV','',self._version,'8.1']
                                   })

        # _headerStyle = CellStyle(bold=True, border=True,bg_color=0x26DEC5)
        #
        #
        # _t = Table("HEADER",_header_df,header_style=_headerStyle)
        #
        #
        # sheet = Worksheet("HEADER")
        # sheet.add_table(_t)
        #
        # workbook = Workbook("example.xlsx")
        # workbook.add_sheet(sheet)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(self._pathName, engine='xlwt')

        # Convert the dataframe to an XlsxWriter Excel object.
        _header_df.to_excel(writer, sheet_name='HEADER', index=False)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    def parse(self):

        print("[MICD]{parse] Parse excel file: " + self._pathName)
        self._dataframe = pd.read_excel(self._pathName)

        print(self._dataframe.index)
        print(self._dataframe.columns)

        xl = pd.ExcelFile(self._pathName)
        print(xl.sheet_names)