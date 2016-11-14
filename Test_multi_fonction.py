import sys

from BDS.BDS2XML import BDS2XML
from BDS.BDS_EIS import BDS_EIS
from BDS.BDS_FWC import BDS_FWC
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD





def main():

    print(sys.argv[1])

    bdsFWC = BDS_FWC(sys.argv[1], sys.argv[5])
    bds2xml_file = BDS2XML(sys.argv[2],True)
    bdsEis = BDS_EIS(sys.argv[3],sys.argv[4])

    print ("**EIS**")
    xml_file = FDEF_XML("test.xml", "A429")
    micdFile = FDEF_MICD("FDEF.xls", "fdef_FWC", 'V1.0')

    labelObjList = bdsFWC.get_LabelObjList(nature="IN", system="FWC")

    for labelObj in labelObjList:
        if len(labelObj.ParameterList) > 0:

            micdFile.AddLabelToMICD(labelObj)

            xml_file.AddLabel(labelObj)
            for parameterObj in labelObj.getParameterList():
                bds2xml_file.AddLine(parameterObj)

    bds2xml_file.savefile()
    xml_file.WriteAndClose()
    micdFile.savefile()

main()


