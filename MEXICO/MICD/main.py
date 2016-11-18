from MEXICO.MICD.MICD_new import MICD_new
from MEXICO.MICD.MICD import MICD
import sys

def main():

    #monMicd = MICD(sys.argv[1], 'MODserge', 'V1.0', True)
    #autreMicd = MICD(sys.argv[2],'prim_a/1','V1.0')

    monMicd = MICD_new(sys.argv[1], 'MODserge', 'V1.0', newfile=True)
    autreMicd = MICD_new(sys.argv[2])
    autreMicd.hasPort("ax_s_9066_52")

    #monMicd.write()
    _port_in = [
        'ax_s_10230_121',
        'int',
        'wu',
        'AFDX FS',
        '',
        '1',
        '1',
        'AFDX',
        'S',
        '',
        '',
        '',
        '',
        '0 / 2 / 4 / 8 / 16 / 32',
        'True',
        'PRIM1A:VL_ADIRU1_GPIRS:ADIRU_GPIRS_AFDX_MSG_1:ADIRU_GPIRS_VELOCITY_DATA_2',
        'Preformat',
        'True',
        'True',
        '0',
        'False',
        'N042011',
        ''
    ]
    _port_out = [
        'ABPOSOUT_50203',
        'float',
        'deg',
        'Speed Brake lever position',
        '',
        '1',
        '1',
        'AFDX',
        'S',
        '',
        '24',
        '- 3',
        '57',
        '',
        'True',
        'VL_PRIM1A_SERVICE:PRIMA_ABPOSOUT_Common_Frame_sg',
        'Preformat',
        'False',
        'True',
        'NFF5010',
        'False',
        '',
        ''
    ]

    #monMicd.AddPortfromTab(_port_in, "IN")
    #monMicd.AddPortfromTab(_port_out, "OUT")
    #monMicd.savefile()

#    for portobject in autreMicd.getPortObjectList():
#        print (portobject.getPortLineTab())

main()