from BDS2XML import BDS2XML
from BDS_FWC import BDS_FWC
from BDS_EIS import BDS_EIS
from FDEF_XML import FDEF_XML

#from MICD import MICD

import sys

def main():

    print(sys.argv[1])

    bds_fwc = BDS_FWC(sys.argv[1],sys.argv[5])
    bds2xml_file = BDS2XML(sys.argv[2],True)
    bdsEis = BDS_EIS(sys.argv[3],sys.argv[4])

    print ("**EIS**")
    xml_file = FDEF_XML("test.xml", "A429")

    labelObjList  = bds_fwc.get_LabelObjList(nature="IN", system="FWC")

    for labelObj in labelObjList:
        if len(labelObj.ParameterList) > 0:
            xml_file.AddLabel(labelObj)
            for parameterObj in labelObj.getParameterList():
                bds2xml_file.AddLine(parameterObj)

    bds2xml_file.savefile()
    xml_file.WriteAndClose()


main()