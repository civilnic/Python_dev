from BDS2XML import BDS2XML
from BDS_FWC import BDS_FWC
from BDS_EIS import BDS_EIS
import sys

def main():

    print(sys.argv[1])

    bds_file=BDS_FWC(sys.argv[1])
    bds2xml_file=BDS2XML(sys.argv[2],True)
   # bds_file.parse_BDS()
 #   bds2xml_file.createemptyfile()
  #  bds2xml_file.savefile()

    bdsEis=BDS_EIS(sys.argv[3],sys.argv[4])


    for system in bds_file.BDS.keys():
        print ("**"+system+"**")
        label_list=list(bds_file.BDS[system]['A429LabelsList'].keys())
        label_list.sort();
        print (label_list)
        #for LabelNumber in bds_file.BDS[system]['A429LabelsList']:
           # print ("\t**"+LabelNumber+"**")
            #label=bds_file.BDS[system]['A429LabelsList'][LabelNumber]
            #for signal in label.signalList:
                #pass
                #print ("signal name: "+signal.name)

    if (bds_file.get_LabelObj('FWC',"008") is not None):
        print (bds_file.get_LabelObj('FWC',"008").type)
    else:
        print ("Label 008 non défini")


main()