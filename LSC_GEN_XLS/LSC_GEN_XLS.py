import sys

from BDS.BDSXLS import BDSXLS
from BDS.BDS_EIS import BDS_EIS
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD
from lxml import etree
import xlrd
import pandas as pd
from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque, A429ParamISO5)



def main():

 # pour creer le fichier .xls à partir de la BDS EIS.

    print("** Parse BDS EIS**")
    bdsEis = BDS_EIS(sys.argv[1])


    xml_conso_file = FDEF_XML("A429_conso_fdef_LSC.xml", "A429")
    xml_prod_file = FDEF_XML("A429_prod_fdef_LSC.xml", "A429")
    micdFile = FDEF_MICD("FDEF_LSC_TCAS.xls", "fdef_LSC", 'V1.0')

    bdsXLS = BDSXLS("BDS_TCAS.xls",new=True)

    #labelObjList = bdsEis.get_LabelObjList(nature="IN", system="EIS", source=r"FCU.*|ADR.*|ILS.*|IRS.*|^FM.*|DME.*|VOR.*|RA.")
    labelObjList = bdsEis.get_LabelObjList(nature="IN", system="EIS", source=r"TCAS.*|DTIF.*")

    for labelObj in labelObjList:

        if len(labelObj.ParameterList) > 0:
             #labelObj.print(DisplayParam=False)
             micdFile.AddLabelToMICD(labelObj)
             xml_prod_file.AddLabel(labelObj)
             for parameterObj in labelObj.getParameterList():
                 bdsXLS.AddLine(parameterObj)


    print("**bds2xml_file save file**")
    bdsXLS.savefile()

    print("**xml_file save file**")
    xml_conso_file.WriteAndClose()
    xml_prod_file.WriteAndClose()

    print("**micdFile save file**")
    micdFile.savefile()

main()
