"""
Tool to generate XML and MICD file for FDEF from a BDS in XLS format.
"""

import logging
import csv

from os.path import abspath
from logging.handlers import RotatingFileHandler
from datetime import datetime
from optparse import OptionParser
from lxml import etree

from BDS.BDSXLS import BDSXLS
from FDEF.FDEF_XML import FDEF_XML
from FDEF.FDEF_MICD import FDEF_MICD

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

#
# global variables
#

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
    parser = OptionParser("usage: %prog --xls <xmlConfigFile> --modName ")
    parser.add_option("--xls", dest="xls", help="bds file (.xls format)",
                      type="string", metavar="FILE")
    parser.add_option("--modName", dest="modName", help="Model name",
                      type="string", metavar="FILE")
    parser.add_option("--version", dest="version", help="version",
                      type="string", metavar="FILE")
    (options, args) = parser.parse_args()

    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _xls = options.xls
    _modName = options.modName
    _version = options.version

    _bdsObj = BDSXLS(path_name=_xls)


    _micdFdef = FDEF_MICD("ICD_"+ _modName + "_" + _version + ".xls",
                          _modName,
                          _version
                             )

    _xml_conso_file = FDEF_XML("A429_conso_" + _modName + "_" + _version + ".xml",
                               "A429",
                               source=_xls,
                               sourceType="BDS",
                               tool="XSL2FDEF"
                               )

    _xml_prod_file = FDEF_XML("A429_prod_" + _modName + "_" + _version + ".xml",
                              "A429",
                              source=_xls,
                              sourceType="BDS",
                              tool="XSL2FDEF"
                              )


    _labelObjList = _bdsObj.get_LabelObjList(nature="IN")

    for _labelObj in _labelObjList:
        if len(_labelObj.ParameterList) > 0:
            _micdFdef.AddLabelToMICD(_labelObj)
            _xml_prod_file.AddLabel(_labelObj)


    _labelObjList = _bdsObj.get_LabelObjList(nature="OUT")

    for _labelObj in _labelObjList:
        if len(_labelObj.ParameterList) > 0:
            _micdFdef.AddLabelToMICD(_labelObj)
            _xml_conso_file.AddLabel(_labelObj)


    print("**xml_file save file**")
    _xml_conso_file.WriteAndClose()
    _xml_prod_file.WriteAndClose()

    print("**micdFile save file**")
    _micdFdef.savefile()

main()