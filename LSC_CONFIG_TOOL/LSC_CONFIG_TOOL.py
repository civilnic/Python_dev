import sys

from BDS.BDSXLS import BDSXLS
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD
from lxml import etree
import xlrd
import pandas as pd
from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque, A429ParamISO5)



class SPEC_FDEF_XML(FDEF_XML):

    def __init__(self, pathname, type, _source="", _sourceType="", _tool=""):
        super().__init__(pathname, type, source=_source, sourceType=_sourceType, tool=_tool)


    def AddParameter(self, ParamObj):

        if isinstance(ParamObj, A429ParamISO5) or isinstance(ParamObj, A429ParamOpaque):
            _parameterElement = etree.SubElement(
                self._LabelCurrentElement,
                "parameter",
                name=ParamObj.comments,
                type="String",
                comment=ParamObj.parameter_def
            )
        else:
            _parameterElement = etree.SubElement(
                self._LabelCurrentElement,
                "parameter",
                name=ParamObj.comments,
                type=ParamObj.codingtype,
                comment=ParamObj.parameter_def
            )

        if isinstance(ParamObj, A429ParamISO5):
            _signalElement = etree.SubElement(
                _parameterElement,
                "signal",
                name=ParamObj.SimuPreFormattedName,
                type=ParamObj.codingtype,
                nbBit=str(ParamObj.nb_bits),
                lsb=str(ParamObj.lsb),
                msb=str(ParamObj.msb),
                signed="0",
                startBit="1",
                comment=ParamObj.parameter_def
            )
        else:
            _signalElement = etree.SubElement(
                _parameterElement,
                "signal",
                name=ParamObj.SimuPreFormattedName,
                type=ParamObj.codingtype,
                nbBit=str(ParamObj.nb_bits),
                lsb=str(ParamObj.lsb),
                msb=str(ParamObj.msb),
                signed=str(ParamObj.signed),
                startBit="1",
                comment=ParamObj.parameter_def
            )

        if isinstance(ParamObj, A429ParamBNR):
            _paramType = "BNR"
        elif isinstance(ParamObj, A429ParamBCD):
            _paramType = "BCD"
        else:
            return None
            #TODO : add other param type specification into XML

        if ParamObj.codingtype == "float":
            etree.SubElement(
                _signalElement,
                "float",
                floatResolution=str(ParamObj.resolution),
                floatCodingType=_paramType
            )
        elif ParamObj.codingtype == "int":
            etree.SubElement(
                _signalElement,
                "integer",
                integerResolution=str(ParamObj.resolution),
                integerCodingType=_paramType
            )
        else:
            ParamObj.print()
            print("[FDEF_XML]{AddPatameter] Unknwon param coding type: " + ParamObj.codingtype)



class BDSModifier:

    def __init__(self, file, paramColumn):
        self._file = file
        self._paramCol = paramColumn
        self._pandaXLS = None
        self._pandaDF = None

        self.changeFile()

    def changeFile(self):

        # specify encoding to avoid unknwon encoding issue
        _xlrd_workbook = xlrd.open_workbook(self._file, encoding_override="cp1252")

        # parse MICD file with pandas
        self._pandaXLS = pd.ExcelFile(_xlrd_workbook, engine="xlrd")

        self._pandaDF = self._pandaXLS.parse("OUT")

        _colList = list(self._pandaDF.columns.values)

        if "Comments" not in _colList:
            raise ValueError('Excel file must contain a <Comments> column')

        if self._paramCol not in _colList:
            raise ValueError(self._paramCol + ' is not in excel column names list')

        # get indexes of comments and Param column in column list name
        _indexComment = _colList.index("Comments")

        # col names to keep in result file
        _coltoKeep = _colList[:_indexComment]

        # intersection with all col name to get col names to delete
        _colToDel = list(filter(lambda x: x not in _coltoKeep, _colList))

        # remove parameter col name from column to del list
        _colToDel.remove(self._paramCol)

        # remove col from dataframe
        self._pandaDF.drop(_colToDel, axis=1, inplace=True)

        # re - compute col list
        _colList = list(self._pandaDF.columns.values)

        # index of param column
        _indexParam = _colList.index(self._paramCol)

        # modify param column name into "Comments"
        _colList[_indexParam] = "Comments"
        self._pandaDF.columns = _colList


    def save(self, file):

        self._pandaDF.to_excel(file, index=False, sheet_name="OUT")







def main():

 # pour creer le fichier .xls à partir de la BDS EIS.


    # bdsEis = BDS_EIS(sys.argv[1])
    #
    #
    # xml_conso_file = FDEF_XML("A429_conso_fdef_eis.xml", "A429")
    # xml_prod_file = FDEF_XML("A429_prod_fdef_eis.xml", "A429")
    # micdFile = FDEF_MICD("FDEF_EIS.xls", "fdef_EIS", 'V1.0')
    #
    # bdsXLS = BDSXLS("BDS_STD14.xls",new=True)
    #
    # labelObjList = bdsEis.get_LabelObjList(nature="IN", system="EIS", source=r"FCU.*|ADR.*|ILS.*|IRS.*|^FM.*|DME.*|VOR.*|RA.")
    # #labelObjList = bdsEis.get_LabelObjList()
    #
    # for labelObj in labelObjList:
    #
    #     if len(labelObj.ParameterList) > 0:
    #          labelObj.print(DisplayParam=False)
    #          micdFile.AddLabelToMICD(labelObj)
    #          xml_prod_file.AddLabel(labelObj)
    #          for parameterObj in labelObj.getParameterList():
    #              bdsXLS.AddLine(parameterObj)
    #
    #
    # print("**bds2xml_file save file**")
    # bdsXLS.savefile()
    #
    # print("**xml_file save file**")
    # xml_conso_file.WriteAndClose()
    # xml_prod_file.WriteAndClose()
    #
    # print("**micdFile save file**")
    # micdFile.savefile()

    _input_file = sys.argv[1]

    _bdsMod = BDSModifier(_input_file, "Param SIMU1")
    _bdsMod.save("test.xls")


    _bdsXLS =BDSXLS("test.xls", new=False)

    xml_conso_file = SPEC_FDEF_XML("A429_conso_fdef.xml", "A429")
    xml_prod_file = SPEC_FDEF_XML("A429_prod_fdef.xml", "A429")
    micdFile = FDEF_MICD("FDEF_CUBParam.xls", "fdef_EIS", 'V1.0')

    labelObjList = _bdsXLS.get_LabelObjList(nature="OUT", system=".*", source=r".*")

    for labelObj in labelObjList:

        if len(labelObj.ParameterList) > 0:
             labelObj.print(DisplayParam=True)
             micdFile.AddLabelToMICD(labelObj)
             xml_prod_file.AddLabel(labelObj)

    print("**xml_file save file**")
    xml_conso_file.WriteAndClose()
    xml_prod_file.WriteAndClose()

    print("**micdFile save file**")
    micdFile.savefile()

main()
