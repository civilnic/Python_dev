import csv
import logging
from logging.handlers import RotatingFileHandler,BaseRotatingHandler

from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

def main():


    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('MEXICO_INTEGRATOR.log', 'w', 1000000, 1)

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
    parser = OptionParser("usage: %prog --csv <csvFile> --mexico <mexicoCfgFile>")
    parser.add_option("-c","--csv", dest="csvFile", help="CSV file containing connexions/inits to integer",
                      type="string", metavar="FILE")
    parser.add_option("-x","--mexico", dest="mexicoCfgFile", help="Mexico configuration file (.xml)",
                      type="string", metavar="FILE")

    (options, args) = parser.parse_args()
    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _csvFile = options.csvFile
    _mexicoCfgFile = options.mexicoCfgFile

    logger.info("_csvFile: "+_csvFile)
    logger.info("_mexicoCfgFile: "+_mexicoCfgFile)

    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(_mexicoCfgFile)

    _mexicoFlowFile = _mexicoCfgObj.getFlowFile()

    logger.info("_mexicoFlowFile: "+_mexicoFlowFile)

    #
    # csv parsing
    #  this function will parse CSV File
    #
    parseCsvFile(_csvFile, _mexicoFlowFile)






#
# csv parsing
#  this function will parse CSV File
#
# column number are variable, the CSV file can have the following header
# MODOCC_PROD;PORT_PROD;SIGNAL;MODOCC_CONSO;PORT_CONSUM;
# MODOCC_PROD;PORT_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM
# MODOCC_PROD;PORT_PROD;MODOCC_CONSO;PORT_CONSUM;
# MODOCC_PROD;PORT_PROD;OP_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM;;OP_CONS
# MODOCC_PROD;PORT_PROD;OP_PROD;TAB_PROD;SIGNAL;INIT;MODOCC_CONSO;PORT_CONSUM;OP_CONS;TAB_PROD
#
def parseCsvFile(csvFile, flowFile):

    file = open(csvFile, "r")

    try:
        #
        # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
        #
        reader = csv.DictReader(file, delimiter=';')

        #
        # read data
        #
        for row in reader:
            if not parseCsvLine(row):
                break;


    finally:
        file.close()


def parseCsvLine(DicoLine):

    _header = DicoLine.keys()

    if not (('MODOCC_PROD' in _header) and ('PORT_PROD' in _header)
        and ('MODOCC_CONSO' in _header) and ('PORT_CONSUM' in _header)):
        logger.error("[CSV HEADER ERROR] CSV file Header must contains at least: MODOCC_PROD;PORT_PROD;MODOCC_CONSO;PORT_CONSUM;")
        return False

    print(DicoLine)
    return True

main()