import re
from MEXICO.MICD.MICD_port import MICD_port
from datetime import datetime

import xlrd
import xlwt


class MICD:
    """
    Class to parse/create MICD
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200; align: horiz justified, shrink_to_fit true, wrap on;border: top thin, right thin, bottom thin, left thin;')
    xls_style_bold = xlwt.easyxf('font: name Arial, bold on, height 200; pattern: pattern solid, fore_color turquoise; border: top thin, right thin, bottom thin, left thin; align: horiz left;')

    file_structure = {
        
        'Excel_sheets':
        {
            'HEADER': ('Identifier', 'Value'),
            'SIM_CTRL_IN': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
            'SIM_CTRL_OUT': ('Name', 'Type', 'Dim1', 'Unit', 'Description', 'Comment'),
            'PROFILE': ('Name', 'Type', 'Dim1', 'Description'),
            'AIRCRAFT_ICD': ('ICD Version', 'ICD File Name', 'Cross Ref File Name'),
            'SIMULATION_LEVEL': ('Platform Code', 'Simulation Level[1]'),
            'FUN_IN': ('Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode', 'From'
                       , "Refresh\nRate", 'Min', 'Max', 'Enum', 'Consumed If', 'Aircraft Signal Name', "Interface\nLevel",
                       'Status (SSM/FS/Refresh)', "Simulation\nLevel[1]", 'Init Value', 'Custom', 'Comment',
                       'Last Modification'),
            'FUN_OUT': ('Name', 'Type', 'Unit', 'Description', 'Convention', 'Dim1', 'Dim2', 'Com Format', 'Com Mode',
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

            for sheet in MICD.file_structure['Excel_sheets'].keys():
                self._SheetAndIndex[sheet] = {}
                self._SheetAndIndex[sheet]['ColIndex'] = 0
                self._SheetAndIndex[sheet]['ColNbr'] = len(list(MICD.file_structure['Excel_sheets'][sheet]))
                self._SheetAndIndex[sheet]['RowIndex'] = 0
                self._SheetAndIndex[sheet]['RowNbr'] = 0
                self._SheetAndIndex[sheet]['Header'] = list(MICD.file_structure['Excel_sheets'][sheet])
                self._SheetAndIndex[sheet]['XlsSheet'] = None

            self.createemptyfile()
        else:
            self.parse()

    def parse(self):

        self._Workbook = xlrd.open_workbook(self._pathName)
        print("[MICD]{parse] Parse excel file: "+self._pathName)

        for _sheetname in self._Workbook.sheet_names():

            _testOnSheetNameFUNIN = re.match(r'(FUN(_\w+)*_IN)', _sheetname)
            _testOnSheetNameFUNOUT = re.match(r'(FUN(_\w+)*_OUT)', _sheetname)

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

            self._SheetAndIndex[_sheetname] = {}
            self._SheetAndIndex[_sheetname]['ColIndex'] = 0
            self._SheetAndIndex[_sheetname]['ColNbr'] = _sheet.ncols
            self._SheetAndIndex[_sheetname]['RowIndex'] = 0
            self._SheetAndIndex[_sheetname]['RowNbr'] = _sheet.nrows
            self._SheetAndIndex[_sheetname]['Header'] = _sheet.row_values(0)
            self._SheetAndIndex[_sheetname]['XlsSheet'] = None

            for _rowidx in range(1, _sheet.nrows):  # Iterate through rows

                _line = _sheet.row_values(_rowidx)

                if _portType == "IN":
                    _micd_config = 'MICD_portObjectConfigurationIN'
                else:
                    _micd_config = 'MICD_portObjectConfigurationOUT'
                _portObject = MICD_port(_line, _portType, MICD.file_structure[_micd_config])

                if not self.AddPort(_portObject):
                    return False
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
        self._SheetAndIndex[_sheet]['XlsSheet'].col(self.file_structure['Excel_sheets'][_sheet].index('Comment')).width = 20000



        # loop to write sim_ctrl_in cell
        for _ident, _value in sorted(_simctrlinDict.items()):

            self.writeCell(_sheet, 'Name', _ident,True)

            for _field in _value:
                self.writeCell(_sheet, self.file_structure['Excel_sheets'][_sheet][_value.index(_field)+1], _field)

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
                self.writeCell(_sheet, self.file_structure['Excel_sheets'][_sheet][_value.index(_field) + 1], _field)

            self._SheetAndIndex[_sheet]['RowIndex'] += 1
            self._SheetAndIndex[_sheet]['RowNbr'] += 1

        # increase col width
        self._SheetAndIndex[_sheet]['XlsSheet'].col(self.file_structure['Excel_sheets'][_sheet].index('Comment')).width = 20000


        return



    def writeCell(self,sheet,field,value,title=None):

        if title is None:
            _styleToApply = MICD.xls_style
        elif title is True:
            _styleToApply = MICD.xls_style_bold
        else:
            _styleToApply = None
        _index = self.file_structure['Excel_sheets'][sheet].index(field)


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

    # add a port on MICD FUN_IN from a tab
    def AddPortfromTab(self,lineTab,portType):

        if portType == "IN":
            _micd_config = 'MICD_portObjectConfigurationIN'
        else:
            _micd_config = 'MICD_portObjectConfigurationOUT'

        _port = MICD_port(lineTab, portType, MICD.file_structure[_micd_config])

        self.AddPortfromPortObject(_port)

    def AddPortfromPortObject(self, MICDportObject):

        if not self.AddPort(MICDportObject):
            return False

        if MICDportObject.type == "IN":
            _sheet = "FUN_IN"
            _micd_config = 'MICD_portObjectConfigurationIN'
        elif MICDportObject.type == "OUT":
            _sheet = "FUN_OUT"
            _micd_config = 'MICD_portObjectConfigurationOUT'
        else:
            print("[MICD][AddPortfromPortObject] Unknown port Type: "+str(MICDportObject.type)+" !!")
            return False

        _portDict = {
            'name': MICDportObject.name,
            'codingtype': MICDportObject.codingtype,
            'unit': MICDportObject.unit,
            'description': MICDportObject.description,
            'convention': MICDportObject.convention,
            'dim1': MICDportObject.dim1,
            'dim2': MICDportObject.dim2,
            'comformat': MICDportObject.comformat,
            'commode': MICDportObject.commode,
            'fromto': MICDportObject.fromto,
            'resfreshrate': MICDportObject.resfreshrate,
            'min': MICDportObject.min,
            'max': MICDportObject.max,
            'enum': MICDportObject.enum,
            'prodconsif': MICDportObject.prodconsif,
            'aircraftsignalname': MICDportObject.aircraftsignalname,
            'interfacelevel': MICDportObject.interfacelevel,
            'status': MICDportObject.status,
            'simulationlevel': MICDportObject.simulationlevel,
            'initdefaultvalue': MICDportObject.initdefaultvalue,
            'notsimudatacustom': MICDportObject.notsimudatacustom,
            'comment': MICDportObject.comment,
            'lastmodification': MICDportObject.lastmodification
        }


        # loop to write port obecjt attributes values in cell
        for _MICDfield in self.file_structure['Excel_sheets'][_sheet]:

            _field = MICD.file_structure[_micd_config][self.file_structure['Excel_sheets'][_sheet].index(_MICDfield)]

            # to escape empty fields
            if _field is not None:

                # retrieve port object attribute from field name with _portDict dictionnaries
                if _field in _portDict.keys():
                    _value = _portDict[_field]
                else:
                    _value = None
            else:
                _value = None

            self.writeCell(_sheet, _MICDfield, _value)

        self._SheetAndIndex[_sheet]['RowIndex'] += 1
        self._SheetAndIndex[_sheet]['RowNbr'] += 1

        return True

    def AddPort(self,MICDportObject):

        if MICDportObject.name == None:
            print("[MICD][AddPortfromPortObject] Cannot add port into MICD: port name is not defined !!")
            return False

        if MICDportObject.name not in self._Ports.keys():
            self._Ports[MICDportObject.name] = MICDportObject

        return True

    def getPortNameList(self):
        return self._Ports.keys()

    def getPortObjectList(self):
        return list(self._Ports.values())

    def hasPort(self, portName):
        if portName in self._Ports:
            return True
        else:
            return False

    def getPortObject(self, portName):
        if self.hasPort(portName):
            return self._Ports[portName]
        else:
            return None