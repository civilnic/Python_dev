import pandas as pd
from datetime import datetime
import xlwt
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
        self._Ports = {}
        self._ACICD = {}
        self._SheetAndDataFrame = {}
        self._Workbook = None

        if self._newFile is True:
            self.createemptyfile()
        else:
            self.parse()

    #
    # the aim of this function is to fill header , simctrlin and sinctrlout sheet and fill headers in other tabs
    #
    def createemptyfile(self):

        # create excel workbook
        self._Workbook = xlwt.Workbook()

        for _sheet in MICD_new.file_structure['Excel_sheets'].keys():

            self._SheetAndDataFrame[_sheet] = {}
            self._SheetAndDataFrame[_sheet]['XlsSheet'] = None
            self._SheetAndDataFrame[_sheet]['DataFrame'] = pd.DataFrame()

            for _colTitle in MICD_new.file_structure['Excel_sheets'][_sheet]:
                _dataFrame = self._SheetAndDataFrame[_sheet]['DataFrame']
                _dataFrame[_colTitle] = ''

            # add sheet in workbook
            self._SheetAndDataFrame[_sheet]['XlsSheet'] = self._Workbook.add_sheet(_sheet)



        # HEADER tab
        _sheet = "HEADER"
        _df = self._SheetAndDataFrame[_sheet]['DataFrame']

        # date computation for information
        _date = datetime.now()
        _displaydate = str(_date.day)+"/"+str(_date.month)+"/"+str(_date.year)

        # Create a Pandas dataframe from some data.
        _df['Identifier'] = ['ACI', 'APP', 'DAT', 'MOD', 'ORG', 'REF', 'VER', 'VIT']
        _df['Value'] = ['', '', _displaydate, self._modelName, 'EYYSEV', '', self._version, '8.1']

        # SIM_CTRL_IN tab
        _sheet = 'SIM_CTRL_IN'
        _df = self._SheetAndDataFrame[_sheet]['DataFrame']

        _df['Name'] = ['F_HOLD', 'F_INIT', 'F_LOAD', 'F_REINIT',
                                            'F_RUN', 'F_UNLOAD', 'V_CETIME', 'V_DELTAT', 'V_Sim_Id']
        _df['Type'] = ['boolean', 'boolean', 'boolean', 'boolean',
                                            'boolean', 'boolean', 'double', 'float', 'char']
        _df['Dim1'] = ['', '', '', '',
                                            '', '', '', '', '256']
        _df['Unit'] = ['wu', 'wu', 'wu', 'wu',
                                            'wu', 'wu', 's', 's', 'wu']
        _df['Description'] = ['HOLD mode input Flag', 'INIT mode input Flag',
                                                'LOAD mode input Flag', 'REINIT mode input Flag',
                                                'RUN mode input Flag', 'UNLOAD mode input Flag',
                                                'Current Environment time', 'Calculation step variable',
                                                'Simulator Identification']
        _df['Comment'] = [ 'TRUE means HOLD mode is required by the environment.\n\
his flag is used to implement the Freeze function or Hold function on certain \
Simulation platforms.',
                                                'TRUE means INIT mode is required by the environment.\n\
In this mode, the model initialises all internal model data.',
                                                'TRUE means LOAD mode is required by the environment: \
the model is authorised to Load specific files [if needed].\n\
In this case, the file names are to be provided in Model PROFILE Descriptor file.',
                                                'TRUE means REINIT mode is required by the environment.\n\
During this mode a specific behaviour is expected from the models which depends\
on the type of platform.',
                                                'TRUE means Normal Execution Simulation',
                                                'TRUE means UNLOAD mode is required by the environment.\n\
True means the model is required to not perform any functional computation\
and to write on output files if required.',
                                                'The current absolute time in seconds of the environment this is to be \
used to check synchronisation of the model and environment if required.',
                                                'Time between two successive model calls in second.\n\
THIS TIME SHALL BE CONTROLLED FROM THE ENVIRONMENT.\
The Value set at initialisation [ when F_INIT is true ] and fixed.',
                                                'Simulator Platform identification set from Environment to models.\
With this variable the Model will know which Simulator it is running on.\n\
This variable is not refreshed in RUN mode.']

        # SIM_CTRL_OUT tab
        _sheet = 'SIM_CTRL_OUT'
        _df = self._SheetAndDataFrame[_sheet]['DataFrame']

        _df['Name'] = ['R_HOLD', 'R_INIT', 'R_LOAD', 'R_REINIT',
                                            'R_RUN', 'F_UNLOAD', 'V_CETIME', 'V_Sim_Id']
        _df['Type'] = ['boolean', 'boolean', 'boolean', 'boolean',
                                            'boolean', 'boolean', 'double', 'char']
        _df['Dim1'] = ['', '', '', '',
                                            '', '', '', '256']
        _df['Unit'] = ['wu', 'wu', 'wu', 'wu',
                                            'wu', 'wu', 's', 'wu']
        _df['Description'] = ["HOLD mode return Flag",
                                                    "INIT mode return Flag",
                                                    "LOAD mode return Flag",
                                                    "REINIT mode return Flag",
                                                    "RUN mode return Flag",
                                                    "UNLOAD mode return Flag",
                                                    "Current Simulation Model time",
                                                    "Model Identification"
                                                    ]
        _df['Comment'] = [
            'If HOLD mode is required (F_HOLD is true) then :\n\
R_HOLD = TRUE means the model is successfully running in Hold mode\n\
R_HOLD = FALSE means an error occurs in execution of HOLD mode tasks',
            'If INIT mode is required (F_INIT is true) then :\n\
R_INIT = TRUE means the model has successfully performed all INIT mode tasks.\n\
R_INIT = FALSE means the model has not performed all INIT tasks required (further calculation steps are necessary).',
            'If LOAD mode is required (F_LOAD is true) then :\n\
R_LOAD = True means the model has successfully loaded the files and performed LOAD mode tasks.\n\
R_LOAD = False means an error occurs in execution of LOAD mode tasks.',
            'If REINIT mode is required (F_REINIT is true) then :\n\
R_REINIT = TRUE means the model has successfully performed the level of stabilisation required.\n\
R_REINIT = FALSE means the model has not yet reached the level of stabilisation required.',
            'If RUN mode is required (F_RUN is true) then :\n\
R_RUN = TRUE means the model is successfully running in Normal RUN mode.\n\
R_RUN = FALSE means an error occurs in execution of RUN mode tasks.',
            'If UNLOAD mode is required (F_UNLOAD is true) then :\n\
R_UNLOAD = TRUE means the model has successfully completed the tasks of the UNLOAD mode.\n\
R_UNLOAD = FALSE means an error occurs in execution of UNLOAD mode tasks.',
            'The current absolute time of the simulation model:\n\
this input is only to be used to check synchronisation of the model and environment if required.\n\
Passed before V_CETIME.',
            'Model identification sent from Models to Environment.\n\
With this variable, the Environment or users can check the issue/date of models\n\
This variable is not refreshed in RUN mode.'
        ]


    def parse(self):

        print("[MICD]{parse] Parse excel file: " + self._pathName)
        self._dataframe = pd.read_excel(self._pathName)

        print(self._dataframe.index)
        print(self._dataframe.columns)

        xl = pd.ExcelFile(self._pathName)
        print(xl.sheet_names)


    def write(self):

        for _sheet in self._SheetAndDataFrame:
            _worksheet = self._SheetAndDataFrame[_sheet]['XlsSheet']
            _dataFrame = self._SheetAndDataFrame[_sheet]['DataFrame']

            for _header in _dataFrame.keys():
                print(_header)
        pass