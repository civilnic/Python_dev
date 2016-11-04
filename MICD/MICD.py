import pathlib
import re
from datetime import datetime
import xlrd, xlwt

class MICD:
    """
    Class to parse/create MICD
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200; align: horiz justified, shrink_to_fit true, wrap on;border: top thin, right thin, bottom thin, left thin;')
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
        for _ident, _value in sorted(_headerDict.items()):

            self.writeCell(_sheet, 'Identifier', _ident,True)
            self.writeCell(_sheet, 'Value', _value)
            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        # fill header sheet
        _sheet = 'SIM_CTRL_IN'

        # create and temp dictonnary it will be used to fill header sheet in a loop
        _simctrlinDict = {'F_HOLD': ["boolean",
                                     "",
                                     "wu",
                                     "HOLD mode input Flag",
                                     'TRUE means HOLD mode is required by the environment.\n\
his flag is used to implement the Freeze function or Hold function on certain \
Simulation platforms.'],
                          'F_INIT': ["boolean",
                                     "",
                                     "wu",
                                     "INIT mode input Flag",
                                     'TRUE means INIT mode is required by the environment.\n\
In this mode, the model initialises all internal model data.'],
                          'F_LOAD': ["boolean",
                                     "",
                                     "wu",
                                     "LOAD mode input Flag",
                                     'TRUE means LOAD mode is required by the environment: \
the model is authorised to Load specific files [if needed].\n\
In this case, the file names are to be provided in Model PROFILE Descriptor file.'],
                          'F_REINIT': ["boolean",
                                     "",
                                     "wu",
                                     "REINIT mode input Flag",
                                     'TRUE means REINIT mode is required by the environment.\n\
During this mode a specific behaviour is expected from the models which depends\
on the type of platform.'],
                          'F_RUN': ["boolean",
                                       "",
                                       "wu",
                                       "RUN mode input Flag",
                                       'TRUE means Normal Execution Simulation'],
                          'F_UNLOAD': ["boolean",
                                       "",
                                       "wu",
                                       "UNLOAD mode input Flag",
                                       'TRUE means UNLOAD mode is required by the environment.\n\
True means the model is required to not perform any functional computation\
and to write on output files if required.'],
                          'V_CETIME': ["double",
                                       "",
                                       "s",
                                       "Current Environment time",
                                       'The current absolute time in seconds of the environment this is to be used to \
check synchronisation of the model and environment if required.'],
                          'V_DELTAT': ["float",
                                       "",
                                       "s",
                                       "Calculation step variable",
                                       'Time between two successive model calls in second.\n\
THIS TIME SHALL BE CONTROLLED FROM THE ENVIRONMENT.\
The Value set at initialisation [ when F_INIT is true ] and fixed.'],
                          'V_Sim_Id': ["char",
                                       "256",
                                       "wu",
                                       "Simulator Identification",
                                       'Simulator Platform identification set from Environment to models.\
With this variable the Model will know which Simulator it is running on.\n\
This variable is not refreshed in RUN mode.']

                          }
        # increase col width
        self._SheetAndIndex[_sheet]['XlsSheet'].col(self.file_structure[_sheet].index('Comment')).width = 20000



        # loop to write sim_ctrl_in cell
        for _ident, _value in sorted(_simctrlinDict.items()):

            self.writeCell(_sheet, 'Name', _ident,True)

            for _field in _value:
                self.writeCell(_sheet, self.file_structure[_sheet][_value.index(_field)+1], _field)

            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        # fill header sheet
        _sheet = 'SIM_CTRL_OUT'

        # create and temp dictonnary it will be used to fill header sheet in a loop
        _simctrloutDict = {'R_HOLD': ["boolean",
                                     "",
                                     "wu",
                                     "HOLD mode return Flag",
                                     'If HOLD mode is required (F_HOLD is true) then :\n\
R_HOLD = TRUE means the model is successfully running in Hold mode\n\
R_HOLD = FALSE means an error occurs in execution of HOLD mode tasks'],
                          'R_INIT': ["boolean",
                                     "",
                                     "wu",
                                     "INIT mode return Flag",
                                     'If INIT mode is required (F_INIT is true) then :\n\
R_INIT = TRUE means the model has successfully performed all INIT mode tasks.\n\
R_INIT = FALSE means the model has not performed all INIT tasks required (further calculation steps are necessary).'],
                          'R_LOAD': ["boolean",
                                     "",
                                     "wu",
                                     "LOAD mode return Flag",
                                     'If LOAD mode is required (F_LOAD is true) then :\n \
R_LOAD = True means the model has successfully loaded the files and performed LOAD mode tasks.\n\
R_LOAD = False means an error occurs in execution of LOAD mode tasks.'],
                          'R_REINIT': ["boolean",
                                       "",
                                       "wu",
                                       "REINIT mode return Flag",
                                       'If REINIT mode is required (F_REINIT is true) then :\n\
R_REINIT = TRUE means the model has successfully performed the level of stabilisation required.\n\
R_REINIT = FALSE means the model has not yet reached the level of stabilisation required.'],
                          'R_RUN': ["boolean",
                                    "",
                                    "wu",
                                    "RUN mode return Flag",
                                    'If RUN mode is required (F_RUN is true) then :\n\
R_RUN = TRUE means the model is successfully running in Normal RUN mode.\n\
R_RUN = FALSE means an error occurs in execution of RUN mode tasks.'],
                          'R_UNLOAD': ["boolean",
                                       "",
                                       "wu",
                                       "UNLOAD mode return Flag",
                                       'If UNLOAD mode is required (F_UNLOAD is true) then :\n\
R_UNLOAD = TRUE means the model has successfully completed the tasks of the UNLOAD mode.\n\
R_UNLOAD = FALSE means an error occurs in execution of UNLOAD mode tasks.'],
                          'V_CMTIME': ["double",
                                       "",
                                       "s",
                                       "Current Simulation Model time",
                                       'The current absolute time of the simulation model:\n\
this input is only to be used to check synchronisation of the model and environment if required.\n\
Passed before V_CETIME.'],
                           'V_Model_Id': ["char",
                                       "256",
                                       "wu",
                                       "Model Identification",
                                       'Model identification sent from Models to Environment.\n\
With this variable, the Environment or users can check the issue/date of models\n\
This variable is not refreshed in RUN mode.']
                          }
        # loop to write sim_ctrl_in cell
        for _ident, _value in sorted(_simctrloutDict.items()):

            self.writeCell(_sheet, 'Name', _ident, True)

            for _field in _value:
                self.writeCell(_sheet, self.file_structure[_sheet][_value.index(_field) + 1], _field)

            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        # increase col width
        self._SheetAndIndex[_sheet]['XlsSheet'].col(self.file_structure[_sheet].index('Comment')).width = 20000


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

