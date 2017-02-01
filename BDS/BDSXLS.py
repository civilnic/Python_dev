import xlwt
import xlrd
from re import match
from BDS.BDS import BDS
from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque, A429ParamISO5)

class BDSXLS(BDS):
    """
    Class to defined BDSXLS input data file
    """
    xls_style = xlwt.easyxf('font: name Arial, bold off, height 200;')

    file_structure = {
        'IN': ['System','A429 Label Name','From','Port Name','Type','Label Number','SDI','Label type','Ssm Type','Parameter Name','Parameter Format','Description','Unit','Parameter MSB','Size','Signed','Range','Bool False Def','Bool True Def','Comments'],
        'OUT': ['System','A429 Label Name','From','Port Name','Type','Label Number','SDI','Label type','Ssm Type','Parameter Name','Parameter Format','Description','Unit','Parameter MSB','Size','Signed','Range','Bool False Def','Bool True Def','Comments']
    }

    def __init__(self, path_name , new=False):
        """
        Attributes are:
        _ path name of the file
        """
        self.new = new
        self.PathName = path_name
        self.Workbook = None
        self.SheetAndIndex = {}

        # heritage of BDS class
        super().__init__()

        if self.new is True:
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
                    _sheet = "IN"
                elif _testOnSheetNameFUNOUT:
                    _sheet = "OUT"

                else:
                    continue

                _worksheet = self._Workbook.sheet_by_name(_sheetname)

                self.SheetAndIndex[_sheetname] = {}
                self.SheetAndIndex[_sheetname]['ColIndex'] = 0
                self.SheetAndIndex[_sheetname]['ColNbr'] = _worksheet.ncols
                self.SheetAndIndex[_sheetname]['RowIndex'] = 0
                self.SheetAndIndex[_sheetname]['RowNbr'] = _worksheet.nrows
                self.SheetAndIndex[_sheetname]['Header'] = _worksheet.row_values(0)
                self.SheetAndIndex[_sheetname]['XlsSheet'] = None

                _fieldList = BDSXLS.file_structure[_sheet]

                for _rowidx in range(1, _worksheet.nrows):  # Iterate through rows

                    _line = _worksheet.row_values(_rowidx)

                    _labelNumber = str("%.3d" % int(_line[_fieldList.index("Label Number")]))

                    LabelObj = A429Label(_labelNumber,
                                         _line[_fieldList.index("SDI")],
                                         _line[_fieldList.index("Label type")],
                                         _sheet,
                                         _line[_fieldList.index("System")]
                                         )

                    LabelObj.source = _line[_fieldList.index("From")]
                    LabelObj.ssmtype = _line[_fieldList.index("Ssm Type")]

                    # ref this labelObject on BDSXLS Obj
                    LabelObj = self.add_Label(LabelObj)

                    LabelObj.SimuFormattedName = _line[_fieldList.index("A429 Label Name")]

                    if _line[_fieldList.index("Parameter Format")] == "BNR":

                        ParamObj = A429ParamBNR(_line[_fieldList.index("Parameter Name")],
                                                _sheet,
                                                _labelNumber,
                                                _line[_fieldList.index("Parameter MSB")],
                                                _line[_fieldList.index("Size")],
                                                _line[_fieldList.index("Range")],
                                                self.ComputeResolutionBNR(_line[_fieldList.index("Size")],
                                                                          _line[_fieldList.index("Range")]
                                                                         )
                        )
                        ParamObj.signed = _line[_fieldList.index("Signed")]

                    elif _line[_fieldList.index("Parameter Format")] == "BCD":

                        ParamObj = A429ParamBCD(_line[_fieldList.index("Parameter Name")],
                                                _sheet,
                                                _labelNumber,
                                                _line[_fieldList.index("Parameter MSB")],
                                                _line[_fieldList.index("Size")],
                                                _line[_fieldList.index("Range")],
                                                self.ComputeResolutionBCD(_line[_fieldList.index("Size")],
                                                                          _line[_fieldList.index("Range")]
                                                                         )
                                                )
                        ParamObj.signed = _line[_fieldList.index("Signed")]

                    elif _line[_fieldList.index("Parameter Format")] == "DW":

                        ParamObj = A429ParamDIS(_line[_fieldList.index("Parameter Name")],
                                                _sheet,
                                                _labelNumber)
                        ParamObj.BitNumber = _line[_fieldList.index("Parameter MSB")]
                        ParamObj.state0 = _line[_fieldList.index("Bool False Def")]
                        ParamObj.state1 = _line[_fieldList.index("Bool True Def")]

                    elif _line[_fieldList.index("Parameter Format")] == "ISO5":

                        ParamObj = A429ParamISO5( _line[_fieldList.index("Parameter Name")],
                                                    _sheet,
                                                    _labelNumber,
                                                    _line[_fieldList.index("Parameter MSB")],
                                                    _line[_fieldList.index("Size")]
                                                 )

                    elif _line[_fieldList.index("Parameter Format")] == "Opaque":

                        ParamObj = A429ParamOpaque( _line[_fieldList.index("Parameter Name")],
                                                    _sheet,
                                                    _labelNumber,
                                                    _line[_fieldList.index("Parameter MSB")],
                                                    _line[_fieldList.index("Size")]
                                                   )

                    else:
                        pass
                        # print ("[BDS_EIS][ParseLine] Type non reconnu: " + DicoLine['FORMAT_PARAM'])


                    ParamObj.formatparam = _line[_fieldList.index("Parameter Format")]
                    ParamObj.comments = _line[_fieldList.index("Comments")]
                    ParamObj.parameter_def = _line[_fieldList.index("Description")]
                    ParamObj.unit = _line[_fieldList.index("Unit")]
                    ParamObj.codingtype = _line[_fieldList.index("Type")]
                    ParamObj.SimuPreFormattedName = _line[_fieldList.index("Port Name")]

                    # reference parameter on current labelObj
                    LabelObj.refParameter(ParamObj)

                    #LabelObj.print(True)

    def __del__(self):
        if self.new is True:
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

        linedict['System'] = LabelObj.system

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

        elif isinstance(ParameterObj, A429ParamOpaque) or isinstance(ParameterObj, A429ParamISO5):

            # 'TAIL'
            linedict['Size'] = ParameterObj.nb_bits

            # 'POSI'
            linedict['Parameter MSB'] = ParameterObj.msb