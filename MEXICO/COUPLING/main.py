from MEXICO.COUPLING.mexico_coupling import mexico_coupling
import sys

def main():

    print(sys.argv[1])
    MexicoCplFile=sys.argv[1]

    _cpl = mexico_coupling(MexicoCplFile)
    _testcpl = None

    for aliasObj in _cpl.getAliasObj():
        if aliasObj.hasOperator() and aliasObj.hasIndice():
            print(aliasObj.operator)
            print(aliasObj.indice)
            print(aliasObj.portname+"\t"+aliasObj.signal+"\t"+aliasObj.date+"\t"+aliasObj.comment+"\t"+aliasObj.sheetname)
            aliasObj.indice = 5
            _testcpl = _cpl
            _testcpl.pathname = './toto.csv'
    if _testcpl:
        _testcpl.write()

main()