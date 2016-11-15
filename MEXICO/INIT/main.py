from MEXICO.INIT.mexico_inits import Mexico_Init_File
import sys

def main():

    print("parametre: "+sys.argv[1])
    mexicoInitFile=sys.argv[1]

    initfile = Mexico_Init_File(mexicoInitFile)

main()