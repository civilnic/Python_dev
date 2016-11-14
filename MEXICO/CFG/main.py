from MEXICO.CFG.mexico_cfg import mexicoConfig
import sys

def main():

    print(sys.argv[1])
    MexicoCfgFile=sys.argv[1]

    cfg = mexicoConfig(MexicoCfgFile)

    for actor in cfg._actors:
        print(actor.name)
   # print(cfg._actors)
main()