"""
Tool to generate XML and MICD file for FDEF from a BDS in XLS2FDEF format (.xls).
Parameters
----------
    --xls <BDS FILE>            -->  BDS file in unified format
    --modName <Model Name>      --> model name for example fdef_sdac/1
    --version <Model version>   --> model version (to be set on MICD)
"""

import logging

from logging.handlers import RotatingFileHandler
from datetime import datetime
from optparse import OptionParser

from BDS.BDSXLS import BDSXLS
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# create logger object
logger = logging.getLogger()

def main():

    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('XLS2FDEF.log', 'w', 1000000, 1)

    # on lui met le niveau sur DEBUG, on lui dit qu'il doit utiliser le formateur
    # créé précédement et on ajoute ce handler au logger
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # création d'un second handler qui va rediriger chaque écriture de log
    # sur la console
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    logger.addHandler(steam_handler)

    # command line treatment
    parser = OptionParser("usage: %prog --xls <xls bds file> --modName <model name> --version <model version>")
    parser.add_option("--xls", dest="xls", help="bds file (.xls format)",
                      type="string", metavar="FILE", default=None)
    parser.add_option("--modName", dest="modName", help="Model name",
                      type="string", metavar="FILE", default=None)
    parser.add_option("--version", dest="version", help="Model version",
                      type="string", metavar="FILE", default=None)
    (options, args) = parser.parse_args()

    _xls = options.xls
    _modName = options.modName
    _version = options.version

    if (_xls is None) or (_modName is None) or (_version is None) or (len(args) == 0):
        parser.error("incorrect number of arguments")


    logger.info("#####################")
    logger.info("#### Parameters #####")
    logger.info("#####################")
    logger.info("# xls file: " + _xls)
    logger.info("# modele name: " + _modName)
    logger.info("# version: " + _version)

    logger.info("Parse BDS (xls file)")
    _bdsObj = BDSXLS(path_name=_xls)

    # output file names
    _micdName = "ICD_" + _modName + "_" + _version + ".xls"
    _xmlIn = "A429_conso_" + _modName + "_" + _version + ".xml"
    _xmlOut = "A429_prod_" + _modName + "_" + _version + ".xml"

    logger.info("Create FDEF MICD: " +_micdName)
    _micdFdef = FDEF_MICD(_micdName,
                          _modName,
                          _version
                          )

    logger.info("Create FDEF xml consumer file: " + _xmlIn)
    _xml_conso_file = FDEF_XML(_xmlIn,
                               "A429",
                               source=_xls,
                               sourceType="BDS",
                               tool="XSL2FDEF"
                               )
    logger.info("Create FDEF xml producer file: " + _xmlOut)
    _xml_prod_file = FDEF_XML(_xmlOut,
                              "A429",
                              source=_xls,
                              sourceType="BDS",
                              tool="XSL2FDEF"
                              )

    logger.info("Create Label IN list and add them into MICD + XML file")
    _labelObjListIN = _bdsObj.get_LabelObjList(nature="IN")

    for _labelObj in _labelObjListIN:
        if len(_labelObj.ParameterList) > 0:
            _micdFdef.AddLabelToMICD(_labelObj)
            _xml_prod_file.AddLabel(_labelObj)

    logger.info("Create Label OUT list and add them into MICD + XML file")
    _labelObjListOUT = _bdsObj.get_LabelObjList(nature="OUT")

    for _labelObj in _labelObjListOUT:
        if len(_labelObj.ParameterList) > 0:
            _micdFdef.AddLabelToMICD(_labelObj)
            _xml_conso_file.AddLabel(_labelObj)


    logger.info("Save XML files")
    _xml_conso_file.WriteAndClose()
    _xml_prod_file.WriteAndClose()

    logger.info("Save MICD file")
    _micdFdef.savefile()

main()