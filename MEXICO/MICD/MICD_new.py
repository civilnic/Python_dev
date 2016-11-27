import pandas as pd
from datetime import datetime
import xlwt, xlrd
import re
from MEXICO.MICD.MICD_port import MICD_port

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
            print("[MICD_new] Create Empty File")
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

        # open with xlrd
        #self._Workbook = xlrd.open_workbook(self._pathName)
        #_sheet = self._Workbook.sheet_by_name(_sheetname)

        # parse MICD file with pandas
        _xl = pd.ExcelFile(self._pathName)

        # loop over MICD sheets name to create dataframe
        for _sheet in _xl.sheet_names:

            # we assume here that MICD sheet name are always the same and equal to
            # MICD_new.file_structure
            # if sheet name is not recognize it's not parsed
            if _sheet not in MICD_new.file_structure['Excel_sheets'].keys():
                print("[MICD] unknown _sheet name: "+_sheet)
                continue

            # create empty dictionnary to store informations
            self._SheetAndDataFrame[_sheet] = {}

            # to store xlrd workbook if write is needed
            self._SheetAndDataFrame[_sheet]['XlsSheet'] = None

            # pandas dataframe of the sheet
            self._SheetAndDataFrame[_sheet]['DataFrame'] = _xl.parse(_sheet)  # create pandas dataframe

            # create corresponding dictionnary for column name
            self._SheetAndDataFrame[_sheet]['ColNameEquiv'] = self.ColumNameEquiv(_sheet)


    def getPortRow(self, portName, type):

        # the parameter type set research sheet
        if type == "IN":
            _sheet = "FUN_IN"
        elif type == "OUT":
            _sheet = "FUN_OUT"
        elif type == "PRF":
            _sheet = "PROFILE"
        else:
            return None

        # sheet data frame
        _df = self._SheetAndDataFrame[_sheet]['DataFrame']

        # column name dict equivalence
        _dict = self._SheetAndDataFrame[_sheet]['ColNameEquiv']

        # port name list of current dataframe
        _portList = list(_df[_dict['Name']])

        if portName in _portList:
            return _df.iloc[_portList.index(portName)]
        else:
            # if not found return None
            return None




    def getPortObj(self, portName):

        _sheet = None

        for _sheet in ["FUN_IN", "FUN_OUT"]:

            # define port type following sheet name
            _type = getPortType(_sheet)

            # get port row
            _portRow = self.getPortRow(portName, _type)

            if _portRow is None:
                continue
            else:
                break

        # if port is not found return None
        if _portRow is None:
            return None

        return self.createPortObj(_portRow, _sheet)


    def getPortObjList(self):

        _PortObjList = []

        for _sheet in ["FUN_IN", "FUN_OUT"]:

            # sheet data frame
            _df = self._SheetAndDataFrame[_sheet]['DataFrame']

            # base on previous list create port object to export
            for _index, _row in _df.iterrows():
                _PortObjList.append(self.createPortObj(_row, _sheet))

        return _PortObjList

    def createPortObj(self, rowDataFrame,sheet):

        # tab to create port Object initialization
        _portTab = []

        # tab to configure sheet
        _cfgTAb = getSheetCfgTab(sheet)

        # define port type following sheet name
        _type = getPortType(sheet)

        # to create port obj we extract from DataFrame only corresponding fields
        # of MICD_portObjectConfigurationIN configuration tab elements
        for _field in MICD_new.file_structure[_cfgTAb]:

            # local var for tab
            _tab = MICD_new.file_structure['Excel_sheets'][sheet]

            # column name dict equivalence
            _dict = self._SheetAndDataFrame[sheet]['ColNameEquiv']

            # index of current _field in column tab
            _index = MICD_new.file_structure[_cfgTAb].index(_field)

            # add
            _portTab.append(rowDataFrame[_dict[_tab[int(_index)]]])

        _portObj = MICD_port(_portTab, _type, MICD_new.file_structure[_cfgTAb])

        return _portObj

    def write(self):

        for _sheet in self._SheetAndDataFrame:
            print("*** [MICD_new] Write: " + _sheet)
            _worksheet = self._SheetAndDataFrame[_sheet]['XlsSheet']
            _dataFrame = self._SheetAndDataFrame[_sheet]['DataFrame']

            print(_dataFrame)
            for _header in _dataFrame.keys():
                print(_header)

    def ColumNameEquiv(self,sheet):

        def callback(str):
            str = str.lower()
            str = str.strip()
            str = re.sub(r'\s','',str)
            str = re.sub(r'\n','',str)
            str = re.sub(r'\t','',str)
            return str

        # dictionnary to fill in this function
        _dict = {}

        # current dataframe
        _df = self._SheetAndDataFrame[sheet]['DataFrame']

        # create a list of current data frame col title without spaces, newline character etc ...
        _dfTitles = list(_df.columns.values)
        _dfTestTitles = list(map(callback, _dfTitles))

        # create the same kind of list on structure file column names
        _colTitles = MICD_new.file_structure['Excel_sheets'][sheet]
        _colTestTitles = list(map(callback,_colTitles))

        # test each value of configuration table
        for _index,_testTitle in enumerate(_colTestTitles):
            if _testTitle in _dfTestTitles:
                _dict[_colTitles[_index]] = _dfTitles[_dfTestTitles.index(_testTitle)]


        return _dict


def getSheetCfgTab(sheet):
    _cfgTAb = None
    if sheet == "FUN_IN":
        _cfgTAb = 'MICD_portObjectConfigurationIN'
    elif sheet == "FUN_OUT":
        _cfgTAb = 'MICD_portObjectConfigurationOUT'
    return _cfgTAb

def getPortType(sheet):
    _type = None
    if sheet == "FUN_IN":
        _type = "IN"
    elif sheet == "FUN_OUT":
        _type = "OUT"
    return _type