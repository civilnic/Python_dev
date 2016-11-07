from MICD import MICD

import sys

def main():

    monMicd = MICD('MICD_serge.xls','MODserge','V1.0',True)

    monMicd.savefile()
main()