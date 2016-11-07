from MICD import MICD

import sys

def main():

    monMicd = MICD('MICD_serge.xls','MODserge','V1.0',True)


    _port_in = [
    'ax_s_10230_121',
    'int',
    'wu',
    'AFDX',
    'FS',
    '1',
    '1',
    'AFDX',
    'S',
    '0 / 2 / 4 / 8 / 16 / 32',
    'True',
    'PRIM1A:VL_ADIRU1_GPIRS:ADIRU_GPIRS_AFDX_MSG_1:ADIRU_GPIRS_VELOCITY_DATA_2',
    'Preformat',
    'True',
    'True',
    '0',
    'False',
    'N042011'
    ]

    monMicd.AddPortfromTab(_port_in,"IN")
    monMicd.savefile()

main()