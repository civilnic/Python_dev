from MEXICO.CFG.mexico_cfg import mexicoConfig
import sys

def main():

    print(sys.argv[1])
    MexicoCfgFile=sys.argv[1]

    cfg = mexicoConfig(MexicoCfgFile)

    for _actorObj in cfg.getActorList():
        print(_actorObj.name)
        for _micdObj in _actorObj.getMICDList():
            print("\t"+_micdObj.fullPathName)
            for _cplObj in _micdObj.getCouplingObjList():
                print("\t\t"+_cplObj.fullPathName)

    _actorObj = cfg.getActor("fcdc/1")
    print(_actorObj.getMICDList())

   # print(cfg._actors)
main()