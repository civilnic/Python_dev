import sys
import csv
import copy
import logging

from logging.handlers import RotatingFileHandler,BaseRotatingHandler
from datetime import datetime
from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig
from FLOT.channel import channel
from FLOT.connexion import PotentialConnexionFromTab
from FLOT.flot import flot
from FLOT.alias import Alias,MexicoAlias
from MEXICO.COUPLING.mexico_coupling import mexico_coupling

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

# CSV current line for logger
line_num = 0

comment = None

#
# dictionary of alias modification to do per model
#
_aliasConsDict = {}
_aliasProdDict = {}
_initializationDict = {}

_mexicoCfgObj = None


def main():

    print('toto')
    global _mexicoCfgObj, comment, logger

    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('BACK2MEXICO.log', 'w', 1000000, 1)

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
    parser = OptionParser("usage: %prog <MexicoCfgFile> <MexicoConceptionFile> <cnxMergeFlowFile> --cmt <comment> ")
    parser.add_option("--cmt", dest="comment", help="Integration comment to add in coupling files",
                      type="string", metavar="FILE")
    (options, args) = parser.parse_args()

    if len(args) != 3:
        logger.info("incorrect number of arguments, mandatory arguments are: <MexicoCfgFile>"
                    " <MexicoConceptionFile> <cnxMergeFlowFile>")
        parser.error("incorrect number of arguments, mandatory arguments are: <MexicoCfgFile>"
                     " <MexicoConceptionFile> <cnxMergeFlowFile>")

    comment = options.comment
    _mexicoCfgFile = sys.argv[1]
    _conceptionFile = sys.argv[2]
    _cnxmFlowFile = sys.argv[3]

    print(args[1])

    logger.info("************************************************")
    logger.info(" BACK2MEXICO tool")
    logger.info("************************************************")
    logger.info(" run informations:")
    logger.info("")
    logger.info(" scripts parameters: ")
    logger.info("\t<MexicoCfgFile> "+_mexicoCfgFile)
    logger.info("\t<MexicoConceptionFile> "+_conceptionFile)
    logger.info("\t<cnxMergeFlowFile> "+_cnxmFlowFile)
    logger.info("\t<comment> "+comment)

    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(_mexicoCfgFile)
    _mexicoCfgObj.conceptionFile = _conceptionFile

    _mexicoFlowFile = _mexicoCfgObj.getFlowFile()

    logger.info(" computed parameters: ")
    logger.info("\tmexico database root path: "+_mexicoCfgObj.getMexicoRootPath())
    logger.info("\tmexico Flow File: "+_mexicoFlowFile)

    #
    # parse MEXICO flow file
    #
    _mexicoFlotObj = flot(_mexicoFlowFile)

    #
    # parse CNXMERGE flow file
    #
    _cnxmFlotObj = flot(_cnxmFlowFile)

    #
    # create model list for each flow
    #
    _mexicoModelList = set(_mexicoFlotObj.getModelList())
    _cnxmModelList = _cnxmFlotObj.getModelList()

    #
    # create common model list
    #
    _commonModels = [x for x in _cnxmModelList if x in _mexicoModelList]


main()