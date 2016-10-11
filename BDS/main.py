from BDS2XML import BDS2XML
from BDS_FWC import BDS_FWC
from BDS_EIS import BDS_EIS

import sys

def main():

    print(sys.argv[1])

    bds_fwc=BDS_FWC(sys.argv[1],sys.argv[5])
    bds2xml_file=BDS2XML(sys.argv[2],True)
   # bds_file.parse_BDS()
 #   bds2xml_file.createemptyfile()
  #  bds2xml_file.savefile()

    bdsEis=BDS_EIS(sys.argv[3],sys.argv[4])


        #for LabelNumber in bds_file.BDS[system]['A429LabelsList']:
           # print ("\t**"+LabelNumber+"**")
            #label=bds_file.BDS[system]['A429LabelsList'][LabelNumber]
            #for signal in label.signalList:
                #pass
                #print ("signal name: "+signal.name)
    print ("**EIS**")

    #labelObjList=bdsEis.get_LabelObjList(nature="IN",source="FWC")
    labelObjList=bds_fwc.get_LabelObjList(nature="IN", system="FWC")
    source_list={}

    for labelObj in labelObjList:
        #labelObj.print(False)
        if (labelObj.number == 10) and (labelObj.source == "EECPW2B"):
            #pass
            labelObj.print(True)
            source_list[labelObj.source]=labelObj
        for parameterObj in labelObj.getParameterList():
            #if (labelObj.number == 10) and (labelObj.source == "EECPW2B"):
                #print ("\t\tparam: "+parameterObj.name)
            bds2xml_file.AddLine(parameterObj)
#    print (sorted(source_list.keys()))
#    print (len(source_list))
    bds2xml_file.savefile()
main()