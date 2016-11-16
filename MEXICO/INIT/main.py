from MEXICO.INIT.mexico_inits import Mexico_Init_File
import sys

def main():

    print("parametre: "+sys.argv[1])
    mexicoInitFile=sys.argv[1]

    initfile = Mexico_Init_File(mexicoInitFile)



    newFile="test_mexico_init.xls"

    newinitfile = Mexico_Init_File(newFile, True)

    for _portname in sorted(initfile.getPortNameList()):
        _portObject = initfile.getPortObject(_portname)
        print(_portObject.getPortLineTab())
        print(_portObject.type)
        newinitfile.AddPortfromPortObject(_portObject)
    newinitfile.savefile()

    newinitfile = Mexico_Init_File(newFile, False)

    for _portname in sorted(newinitfile.getPortNameList()):
        _portObject = newinitfile.getPortObject(_portname)
        print(_portObject.getPortLineTab())
        print(_portObject.type)
        newinitfile.AddPortfromPortObject(_portObject)
    newinitfile.savefile()

main()