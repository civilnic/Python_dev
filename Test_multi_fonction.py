import sys

from BDS.BDS2XML import BDS2XML
from BDS.BDS_EIS import BDS_EIS
from BDS.BDS_FWC import BDS_FWC
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD





def main():

    print(sys.argv[1])

    bdsFWC = BDS_FWC(sys.argv[1], sys.argv[5])
    bds2xml_file = BDS2XML("_tests_results/"+sys.argv[2],True)
    bdsEis = BDS_EIS(sys.argv[3],sys.argv[4])
#    print ("**EIS**")

    #xml_conso_file = FDEF_XML("_tests_results/A429_conso_fdef_fwc.xml", "A429")
    #xml_prod_file = FDEF_XML("_tests_results/A429_prod_fdef_fwc.xml", "A429")
    #micdFile = FDEF_MICD("_tests_results/FDEF_FWC.xls", "fdef_FWC", 'V1.0')

    xml_conso_file = FDEF_XML("_tests_results/A429_conso_fdef_eis.xml", "A429")
    xml_prod_file = FDEF_XML("_tests_results/A429_prod_fdef_eis.xml", "A429")
    micdFile = FDEF_MICD("_tests_results/FDEF_EIS.xls", "fdef_EIS", 'V1.0')


    # OK for FWC
    #labelObjList = bdsFWC.get_LabelObjList(nature="IN", system="FWC", source=r"EEC..|EIU.|ADC.|LGCIU.|FQI.A_.B|ILS.|RA.|GPS.|GPS..|SDCU.|SYNC_\w_\w{3}")


    labelObjList = bdsEis.get_LabelObjList(nature="IN", system="EIS", source=r"ADF.*|ADR.*|CFDIU|DME.*|EEC.*|FQI.|ILS.|IRS.|LGC.|TCAS|VOR.|RA.")

    for labelObj in labelObjList:

        if len(labelObj.ParameterList) > 0:
             micdFile.AddLabelToMICD(labelObj)
             xml_prod_file.AddLabel(labelObj)
             for parameterObj in labelObj.getParameterList():
                 bds2xml_file.AddLine(parameterObj)


    print("**bds2xml_file save file**")
    bds2xml_file.savefile()

    print("**xml_file save file**")
    xml_conso_file.WriteAndClose()
    xml_prod_file.WriteAndClose()

    print("**micdFile save file**")
    micdFile.savefile()

main()


