import xlrd, xlwt
import re
from A429 import (A429Parameter,A429Label,A429ParamDIS,A429ParamBNR,A429ParamBCD,A429ParamOpaque)

class BDS2XML:
    """
    Class to defined BDS2XML input data file
    """
    xls_style=xlwt.easyxf('font: name Arial, bold off, height 200;')

    file_structure = {
        'toEIS':('Model from','Name PF','Type','Name F','NOM_SUPP','CONT','NOM_BLOC','FORMAT_BLOC','LIB_BLOC','SSM_TYPE','NOM_PARAM','FORMAT_PARAM','LIB_PARAM','UNITE','TYPE','POSI','TAIL','SGN','ECHEL','DOMAINE','ETAT_0','ETAT_1','ERREUR','Version BDS','Comments'),
        'fromEIS':('Model from','Name PF','Type','Name F','NOM_SUPP','CONT','NOM_BLOC','FORMAT_BLOC','LIB_BLOC','SSM_TYPE','NOM_PARAM','FORMAT_PARAM','LIB_PARAM','UNITE','TYPE','POSI','TAIL','SGN','ECHEL','DOMAINE','ETAT_0','ETAT_1','ERREUR','Version BDS','Comments'),
        'toFWC(BNR)':('Model from','Name PF','Type','Name F','SW_IDENT','IDENT','NATURE','TYPE','SIG_BIT','RANG_IN','RESOLUTION_IN','UNIT_IN','FORMAT','PAR_DEF','WIRE_NAME_IN','LABEL_IN','SDI_IN','IN_TRANS','FULLSC','Version BDS','Comments'),
        'fromFWC(BNR)':('Model from','Name PF','Type','Name F','SW_IDENT','IDENT','NATURE','TYPE','SIG_BIT','RANG_OUT','RESOLUTION_OUT','UNIT_OUT','FORMAT','PAR_DEF','WIRE_NAME_OUT','LABEL_OUT','SDI_OUT','OUT_TRANS','FULLSC','Version BDS','Comments'),
        'toFWC(DIS)':('Model from','Name PF','Type','Name F','SW_IDENT','IDENT','NATURE','TYPE','IN_TYPE','PAR_DEF','STATE1_IN','STATE0_IN','WIRE_NAME_IN','LABEL_IN','SDI_IN','BIT_IN','IN_TRANS','Version BDS','Comments'),
        'fromFWC(DIS)':('Model from','Name PF','Type','Name F','SW_IDENT','IDENT','NATURE','TYPE','OUT_TYPE','PAR_DEF','STATE1_OUT','STATE0_OUT','WIRE_NAME_OUT','LABEL_OUT','SDI_OUT','BIT_OUT','OUT_TRANS','Version BDS','Comments'),
        'toSDAC':('Model from','Name PF','Type','Name F','Ident','wire_name_in','wire_name_out','nature','in_type','type','label_in','label_out','sdi_in','sdi_out','bit_in','bit_out','in_trans','out_trans','par_definition','format','first_bit','sig_bit','range_out','Version BDS','Comments'),
        'fromSDAC':('Model from','Name PF','Type','Name F','Ident','wire_name_in','wire_name_out','nature','in_type','type','label_in','label_out','sdi_in','sdi_out','bit_in','bit_out','in_trans','out_trans','par_definition','format','first_bit','sig_bit','range_out','Version BDS','Comments')
    }

    def __init__(self, path_name,new):
        """
        Attributes are:
        _ path name of the file
        """
        self.PathName = path_name
        self.Workbook =None
        self.SheetAndIndex={}

        if new is True:
            for sheet in BDS2XML.file_structure.keys():
                self.SheetAndIndex[sheet]={}
                self.SheetAndIndex[sheet]['ColIndex']=0
                self.SheetAndIndex[sheet]['ColNbr']=len(list(BDS2XML.file_structure[sheet]))
                self.SheetAndIndex[sheet]['RowIndex']=0
                self.SheetAndIndex[sheet]['RowNbr']=0
                self.SheetAndIndex[sheet]['Header']=list(BDS2XML.file_structure[sheet])
                self.SheetAndIndex[sheet]['XlsSheet']=None

            self.createemptyfile()

        else:
            pass
            #TODO: initialisation de la classe BDS2XML sur un fichier existant: parsing et initialisation des index

    def __del__(self):
        self.savefile()

    def createemptyfile(self):
        """
        Method to create an empty BDS2XML input file
        :return True/False:
        """
        self.Workbook=xlwt.Workbook()

        for sheet in self.SheetAndIndex:

            # add sheet in workbook
            self.SheetAndIndex[sheet]['XlsSheet'] = self.Workbook.add_sheet(sheet)

            # header creation
            for header_cell in list(self.SheetAndIndex[sheet]['Header']):
                self.SheetAndIndex[sheet]['XlsSheet'].write(self.SheetAndIndex[sheet]['RowIndex'], self.SheetAndIndex[sheet]['ColIndex'], header_cell, BDS2XML.xls_style)
                self.SheetAndIndex[sheet]['ColIndex'] += 1

            # update object information
            self.SheetAndIndex[sheet]['ColIndex'] = 0
            self.SheetAndIndex[sheet]['RowIndex'] += 1
            self.SheetAndIndex[sheet]['RowNbr'] += 1

    def AddLine(self, ParameterObj):

        linedict = dict()

        # wich tab must be filled with parameter values
        LabelObj = ParameterObj.labelObj

        testFWC = re.compile(r"\w*FWC\w*")
        testEIS = re.compile(r"\w*EIS\w*")
        testSDAC = re.compile(r"\w*SDAC\w*")

        if testEIS.search(LabelObj.system):
            if LabelObj.nature == "IN":
                sheet = "toEIS"
            elif LabelObj.nature == "OUT":
                sheet = "fromEIS"
            else:
                print("Unknwon label nature: "+LabelObj.nature)
            self.fillEISLineDict(ParameterObj, linedict)

        elif testFWC.search(LabelObj.system):
            if LabelObj.nature == "IN":
                if LabelObj.labeltype == "DW":
                    sheet = "toFWC(DIS)"
                elif LabelObj.labeltype == "BNR":
                    sheet = "toFWC(BNR)"
                else:
                    print("Unknwon label type: " + LabelObj.labeltype)
                    return None
            elif LabelObj.nature == "OUT":
                if LabelObj.labeltype == "DW":
                    sheet = "fromFWC(DIS)"
                elif LabelObj.labeltype == "BNR":
                    sheet = "fromFWC(BNR)"
                else:
                    print("Unknwon label type: " + LabelObj.labeltype)
                    return None
            else:
                print("Unknwon label nature: " + LabelObj.nature)
            LabelObj.print(False)
            print (type(LabelObj))
            print (type(ParameterObj))

            self.fillFWCLineDict(ParameterObj, linedict)

        elif testSDAC.search(LabelObj.system):
            if LabelObj.nature == "IN":
                sheet = "toSDAC"
            elif LabelObj.nature == "OUT":
                sheet = "fromSDAC"

        else:
            print("[BDS2XML creation] Cannot set tab")
            return None


        for field in linedict.keys():
            self.writeCell(sheet, field, linedict[field])

        self.SheetAndIndex[sheet]['ColIndex'] = 0
        self.SheetAndIndex[sheet]['RowIndex'] += 1

    def writeCell(self, sheet, field, value):

        print("sheet: "+sheet)
        print("field: "+field)
        print("field: "+str(self.file_structure[sheet]))

        index = self.file_structure[sheet].index(field)

        self.SheetAndIndex[sheet]['XlsSheet'].write(self.SheetAndIndex[sheet]['RowIndex'],
                                                    index,
                                                    value,
                                                    BDS2XML.xls_style
                                                    )
        self.SheetAndIndex[sheet]['ColIndex'] += 1


    def savefile(self):
        """
        Method to save a BDS2XML tool input file from BDS2XML current object
        :return True/False:
        """
        self.Workbook.save(self.PathName)


    def fillEISLineDict(self, ParameterObj, linedict):

        LabelObj=ParameterObj.labelObj

        # 'Model from'
        linedict['Model from'] = "SIMU"

        # 'Name PF',
        linedict['Name PF'] = ParameterObj.SimuPreFormattedName

        # 'Type'
        linedict['Type'] = ParameterObj.codingtype

        # 'Name F'
        linedict['Name F'] = LabelObj.SimuFormattedName

        # 'NOM_SUPP'
        linedict['NOM_SUPP'] = LabelObj.source
        #  'CONT'
        linedict['CONT'] = str(LabelObj.number) + "_" + str(LabelObj.sdi)
        # 'NOM_BLOC'
        linedict['NOM_BLOC'] = ParameterObj.nombloc
        # 'FORMAT_BLOC'
        linedict['FORMAT_BLOC'] = LabelObj.labeltype
        # 'LIB_BLOC'
        linedict['LIB_BLOC'] = ParameterObj.libbloc
        # 'SSM_TYPE'
        linedict['SSM_TYPE'] = LabelObj.ssmtype
        # 'NOM_PARAM'
        linedict['NOM_PARAM'] = ParameterObj.name
        # 'FORMAT_PARAM'
        if ParameterObj.formatparam:
            linedict['FORMAT_PARAM'] = ParameterObj.formatparam
        else:
            linedict['FORMAT_PARAM'] = LabelObj.labeltype
        # 'LIB_PARAM'
        linedict['LIB_PARAM'] = ParameterObj.comments
        # 'UNITE'
        linedict['UNITE'] = ParameterObj.unit
        # 'TYPE'
        linedict['TYPE'] = ParameterObj.parameter_def

        if LabelObj.labeltype == "DW":
            # 'ETAT_0'
            linedict['ETAT_0'] = ParameterObj.state0
            # 'ETAT_1'
            linedict['ETAT_1'] = ParameterObj.state1
            # 'TAIL'
            linedict['TAIL'] = 1
            # 'POSI'
            linedict['POSI'] = ParameterObj.BitNumber
        else:
            # 'TAIL'
            linedict['TAIL'] = ParameterObj.nb_bits
            if ParameterObj.formatparam != "DW":
                # 'POSI'
                linedict['POSI'] = ParameterObj.msb
            else:
                # 'POSI'
                linedict['POSI'] = ParameterObj.BitNumber
            if LabelObj.labeltype != "ISO5" and ParameterObj.formatparam != "DW":
                # 'SGN'
                linedict['SGN'] = ParameterObj.signed
                # 'ECHEL'
                linedict['ECHEL'] = ParameterObj.range

                #  'DOMAINE'
                # 'ERREUR'
                #  'Version BDS'
                #  'Comments'

    def fillFWCLineDict(self,  ParameterObj, linedict):

        LabelObj=ParameterObj.labelObj

        print (LabelObj.source   )

        # 'Model from'
        linedict['Model from'] = "SIMU"

        # 'Name PF',
        linedict['Name PF'] = ParameterObj.SimuPreFormattedName

        # 'Type'
        linedict['Type'] = ParameterObj.codingtype

        # 'Name F'
        linedict['Name F'] = LabelObj.SimuFormattedName

        # 'SW_IDENT'
        linedict['SW_IDENT'] = LabelObj.SimuFormattedName

        # 'IDENT'
        linedict['IDENT'] = ParameterObj.name

        # 'TYPE'
        linedict['TYPE'] = ParameterObj.codingtype

        # 'PAR_DEF'
        linedict['PAR_DEF'] = ParameterObj.parameter_def

        if LabelObj.nature == "IN":

            # 'NATURE'
            linedict['NATURE'] = "I"

            # 'SDI_IN'
            linedict['SDI_IN'] = LabelObj.sdi

            # 'LABEL_IN'
            linedict['LABEL_IN'] = LabelObj.number

            # 'WIRE_NAME_IN'
            linedict['WIRE_NAME_IN'] = LabelObj.source

            # 'IN_TRANS'
            linedict['IN_TRANS'] = LabelObj.input_trans_rate

            if LabelObj.labeltype != "DW" and ParameterObj.formatparam != "":

                # 'SIG_BIT'
                linedict['SIG_BIT'] = ParameterObj.nb_bits

                # 'RANG_IN'
                linedict['RANG_IN'] = ParameterObj.range

                # 'RESOLUTION_IN'
                linedict['RESOLUTION_IN'] = ParameterObj.resolution

                # 'UNIT_IN'
                linedict['UNIT_IN'] = ParameterObj.unit

                # 'FORMAT'
                linedict['FORMAT'] = ParameterObj.formatparam

            else:

                # 'IN_TYPE'
                linedict['IN_TYPE'] = "I"

                # 'STATE1_IN'
                linedict['STATE1_IN'] = ParameterObj.state1

                # 'STATE0_IN'
                linedict['STATE0_IN'] = ParameterObj.state0

                # 'BIT_IN'
                linedict['BIT_IN'] = ParameterObj.BitNumber

        else:
            # 'NATURE'
            linedict['NATURE'] = "O"

            # 'SDI_OUT'
            linedict['SDI_OUT'] = LabelObj.sdi

            # 'LABEL_OUT'
            linedict['LABEL_OUT'] = LabelObj.number

            # 'WIRE_NAME_OUT'
            linedict['WIRE_NAME_OUT'] = LabelObj.source

            # 'OUT_TRANS'
            linedict['OUT_TRANS'] = LabelObj.input_trans_rate

            if LabelObj.labeltype != "DW":

                # 'SIG_BIT'
                linedict['SIG_BIT'] = ParameterObj.nb_bits

                # 'RANG_OUT'
                linedict['RANG_OUT'] = ParameterObj.range

                # 'RESOLUTION_OUT'
                linedict['RESOLUTION_OUT'] = ParameterObj.resolution

                # 'UNIT_OUT'
                linedict['UNIT_OUT'] = ParameterObj.unit

                # 'FORMAT'
                linedict['FORMAT'] = ParameterObj.formatparam

            else:

                # 'OUT_TYPE'
                linedict['OUT_TYPE'] = "O"

                # 'STATE1_OUT'
                linedict['STATE1_OUT'] = ParameterObj.state1

                # 'STATE0_OUT'
                linedict['STATE0_OUT'] = ParameterObj.state0

                # 'BIT_OUT'
                linedict['BIT_OUT'] = ParameterObj.BitNumber

#'toFWC(BNR)':
# ('Model from', 'Name PF', 'Type', 'Name F', 'SW_IDENT', 'IDENT', 'NATURE', 'TYPE', 'SIG_BIT','RANG_IN', 'RESOLUTION_IN', 'UNIT_IN', 'FORMAT', 'PAR_DEF', 'WIRE_NAME_IN', 'LABEL_IN',
#                          'SDI_IN', 'IN_TRANS', 'FULLSC', 'Version BDS', 'Comments'),
# 'fromFWC(BNR)':
# ('Model from', 'Name PF', 'Type', 'Name F', 'SW_IDENT', 'IDENT', 'NATURE', 'TYPE', 'SIG_BIT','RANG_OUT', 'RESOLUTION_OUT', 'UNIT_OUT', 'FORMAT', 'PAR_DEF', 'WIRE_NAME_OUT', 'LABEL_OUT',
#                           'SDI_OUT', 'OUT_TRANS', 'FULLSC', 'Version BDS', 'Comments'),
#'toFWC(DIS)':
# ('Model from', 'Name PF', 'Type', 'Name F', 'SW_IDENT', 'IDENT', 'NATURE', 'TYPE', 'IN_TYPE','PAR_DEF', 'STATE1_IN', 'STATE0_IN', 'WIRE_NAME_IN', 'LABEL_IN', 'SDI_IN', 'BIT_IN',
#                          'IN_TRANS', 'Version BDS', 'Comments'),
# 'fromFWC(DIS)':(
#'Model from', 'Name PF', 'Type', 'Name F', 'SW_IDENT', 'IDENT', 'NATURE', 'TYPE', 'OUT_TYPE','PAR_DEF', 'STATE1_OUT', 'STATE0_OUT', 'WIRE_NAME_OUT', 'LABEL_OUT', 'SDI_OUT', 'BIT_OUT',
#                           'OUT_TRANS', 'Version BDS', 'Comments'),
