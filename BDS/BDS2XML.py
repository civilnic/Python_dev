
import xlrd, xlwt

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
                self.SheetAndIndex[sheet]['ColIndex']+=1

            # update object information
            self.SheetAndIndex[sheet]['RowIndex'] += 1
            self.SheetAndIndex[sheet]['RowNbr'] += 1


    def savefile(self):
        """
        Method to save a BDS2XML tool input file from BDS2XML current object
        :return True/False:
        """
        self.Workbook.save(self.PathName)