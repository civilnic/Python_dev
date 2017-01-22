import sys
import csv
import copy
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler,BaseRotatingHandler
from datetime import datetime

from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig
from FLOT.channel import channel
from FLOT.connexion import PotentialConnexionFromTab
from FLOT.flot import flot
from FLOT.alias import MexicoAlias
from MEXICO.COUPLING.mexico_coupling import mexico_coupling
from MEXICO.INIT.mexico_inits import Mexico_Init_File
from MEXICO.MICD.MICD_port import INIT_port
from MEXICO.MICD.MICD import MICD

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

# comment to add in coupling/init files
globalComment = ""

# dictionary to store initialization
_initializationDictPerModel = {}

def main():

    global _mexicoCfgObj, globalComment, channelEYCNameFlag, forceChannelNameFlag, forceInitFlag

    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('INIT_FEEDBACK.log', 'w', 1000000, 1)

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
    parser = OptionParser("usage: %prog --xls <xlsFile> --mexico <mexicoCfgFile> --cp <mexicoconceptionFile>")
    parser.add_option("--xls", dest="xlsFile", help="XLS file containing inits to feedback to MEXICO base",
                      type="string", metavar="FILE")
    parser.add_option("--mexico", dest="mexicoCfgFile", help="Mexico configuration file (.xml)",
                      type="string", metavar="FILE")
    parser.add_option("--cp", dest="mexicoConceptionFile", help="Mexico conception file (.xml)",
                      type="string", metavar="FILE")
    parser.add_option("--cmt", dest="Comment", help="Comment to add in coupling and init files",
                      type="string")
    parser.add_option("--fuselage", dest="fuselage", help="aircraft selection (A319/A320/A321)")
    parser.add_option("--motorization", dest="motorization", help="motorisation selection (PW/CFM)")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _xlsFile = options.xlsFile
    _mexicoCfgFile = options.mexicoCfgFile
    _conceptionFile = options.mexicoConceptionFile
    _globalComment = options.Comment
    _fuselage = options.fuselage
    _motorization = options.motorization


    logger.info("_xlsFile: "+_xlsFile)
    logger.info("_mexicoCfgFile: "+_mexicoCfgFile)
    logger.info("_conceptionFile: "+_conceptionFile)
    logger.info("_fuselage: "+_fuselage)
    logger.info("_motorisation: "+_motorization)
    logger.info("_globalComment: "+_globalComment)

    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(_mexicoCfgFile)
    _mexicoCfgObj.conceptionFile = _conceptionFile

    # parse MEXICO flow file
    _mexicoFlowFile = _mexicoCfgObj.getFlowFile()

    logger.info("_mexicoFlowFile: "+_mexicoFlowFile)

    #
    # csv parsing
    #  this function will parse CSV File
    #
    parseXlsFile(_xlsFile, _mexicoFlowFile)


def parseXlsFile(xlsFile, _xlsFile):

    global _fuselage, _motorization

    # parse MICD file with pandas
    _xl = pd.ExcelFile(_xlsFile)

    # init dataframe
    _df = _xl.parse("Inits")

    for index, row in _df.iterrows():

        _modocc = row['Model/Occ']
        _port = row['Port']

        _initValueCellName = _fuselage + "_" + _motorization
        _value = row[_initValueCellName]

        if _modocc not in _initializationDictPerModel.keys():
            _initializationDictPerModel[_modocc] = {}

        if _port not in _initializationDictPerModel[_modocc].keys():
            _initializationDictPerModel[_modocc][_port] = _value
        else:
            logger.warning("[INIT_FEEDBACK]: Several value specified for port: " + _port +
                           " previous value: " +  _initializationDictPerModel[_modocc][_port])




main()