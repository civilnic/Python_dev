import sys
import csv
import logging
from logging.handlers import RotatingFileHandler,BaseRotatingHandler

from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig
from FLOT.connexion import PotentialConnexionFromTab
from FLOT.flot import flot

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

# EYC channel naming rules flag
channelEYCName = False

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
#
# csv parsing
#  this function will parse CSV File
#
# column number are variable, the CSV file can have the following header
# MODOCC_PROD;PORT_PROD;SIGNAL;MODOCC_CONS;PORT_CONS;
# MODOCC_PROD;PORT_PROD;SIGNAL;INIT;MODOCC_CONS;PORT_CONS
# MODOCC_PROD;PORT_PROD;MODOCC_CONS;PORT_CONS;
# MODOCC_PROD;PORT_PROD;OP_PROD;SIGNAL;INIT;MODOCC_CONS;PORT_CONS;OP_CONS
# MODOCC_PROD;PORT_PROD;OP_PROD;TAB_PROD;SIGNAL;INIT;MODOCC_CONS;PORT_CONS;OP_CONS;TAB_CONS
#
#

def parseCsvFile(csvFile, flowFile):

    file = open(csvFile, "r")

    try:

        #
        # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
        #
        reader = csv.DictReader(file, delimiter=';')

        #
        # get and check the configuration of CSV file
        # i.e the header fields available on CSV
        # see. getCsvParameterTab function to see available fields
        #
        _csvConfTab = getCsvParameterTab(reader.fieldnames)

        #
        # parse flow file to analyse and check CSV file
        #
        _flotObj = flot(flowFile)

        #
        # dictionary of alias modification to do per model
        #
        _aliasTodoCons = {}
        _aliasTodoProd = {}

        #
        # read data
        #
        for row in reader:

            # flag to detect all errors on a line and to reject it if necessary
            _errorFlag = False

            # create connexion object
            _cnxCSVObj = parseCsvLine(row)

            #
            # check essential element of potental connexion: mod_prod / port_prod / mod_cons / port_cons
            #
            if _cnxCSVObj.modoccProd:
                if not _flotObj.hasModele(_cnxCSVObj.modoccProd):
                    logger.error("[CheckCSV][line "+str(reader.line_num)+"] Producer model didn't exist in flow: "+
                                 _cnxCSVObj.modoccProd)
                    _errorFlag = True
                elif _cnxCSVObj.getProdTriplet():
                    if not _flotObj.hasPort(_cnxCSVObj.getProdTriplet()):
                        logger.error("[CheckCSV][line "+str(reader.line_num)+"] Producer port didn't exist in flow: "+
                                     _cnxCSVObj.getProdTriplet())
                        _errorFlag = True
            if _cnxCSVObj.modoccCons:
                if not _flotObj.hasModele(_cnxCSVObj.modoccCons):
                    logger.error("[CheckCSV][line "+str(reader.line_num)+"] Consummer model didn't exist in flow: "+
                                 _cnxCSVObj.modoccCons)
                    _errorFlag = True
                elif _cnxCSVObj.getConsTriplet():
                    if not _flotObj.hasPort(_cnxCSVObj.getConsTriplet()):
                        logger.error("[CheckCSV][line "+str(reader.line_num)+"] Consummer port didn't exist in flow: "+
                                     _cnxCSVObj.getConsTriplet())
                        _errorFlag = True

            if _errorFlag:
                logger.error("[CheckCSV][line "+str(reader.line_num)+"] -- This line is rejected --")
                continue

            #
            # We test if the connection (_cnxCSVObj) from CSV is already set in MEXICO flow
            #   the function compCnx of flow object return a array of boolean;
            #   Each boolean correspond to a field of connextion object (True = field is different)
            #   for example:
            #   [MODOCC_PROD;PORT_PROD;OP_PROD;TAB_PROD;SIGNAL;INIT;MODOCC_CONS;PORT_CONS;OP_CONS;TAB_CONS]
            #   [False, False, False, False, False, True, False, False, False, False]
            #   => INIT field is different

            # if tab is filled with False => there is no difference => nothing to do
            _testTab = _flotObj.compCnx(_cnxCSVObj)

            # if EYC channel name option is activated
            # channel difference is taken into account even if channel name is not specified into CSV file (i.e.
            # _csvConfTab[4] = False)
            # to consider channel name difference _csvConfTab[4] if forced to True
            if channelEYCName:
                _csvConfTab[4] = True

            # differences analysis and translation in term of aliases on modele/port
            if _testTab != [False] * 10:

                # get equivalent (for the same consummer model/port) cnx object in flow file
                _cnxFLOWObj = _flotObj.getCnxForPort(_cnxCSVObj.modoccCons)

                # a differnce on MOD_CONS or PORT_CONS is not possible
                # due to the cnxObj comparison nature (it construct from the same
                # MOD_CONS and PROD_CONS)
                if (_testTab[6] and _csvConfTab[6]) or (_testTab[7] and _csvConfTab[7]):
                    logger.error("[CheckCSV][line " + str(reader.line_num) + "] -- ERROR on Treatment: this case is"
                                                                             "not possible --")
                    continue


                # a difference on one of these fields MODOCC_PROD;PORT_PROD;OP_PROD;TAB_PROD;SIGNAL
                # implies a modification on model producer coupling file
                # and maybe on several other consumer coupling file
                if (_testTab[0] and _csvConfTab[0]) or (_testTab[1] and _csvConfTab[1]) or \
                        (_testTab[2]  and _csvConfTab[2]) or (_testTab[3] and _csvConfTab[3]) or \
                        (_testTab[4] and _csvConfTab[4]):

                    # there is a channel name difference
                    if _testTab[4] and _csvConfTab[4]:

                        # there is a difference on producer model
                        if _testTab[0] and _csvConfTab[0]:

                            #
                            # if difference concern only signal name => it's only a channel renaming
                            #


                            pass
                    # no difference on signal name
                    # signal name used is flow signal name
                    else:

                        pass





                    # if model is not referenced in dictionary => add it
                    if _cnxCSVObj.modoccProd not in _aliasTodoProd.keys():
                        _aliasTodoProd[_cnxCSVObj.modoccProd]=[]

                    # add alias object in tab
                    if _cnxCSVObj.getConsAlias() not in _aliasTodoProd[_cnxCSVObj.modoccProd]:
                        _aliasTodoProd[_cnxCSVObj.modoccProd].append(_cnxCSVObj.getProdAlias())

                    pass


                # a difference on SIGNAL or OP_CONS or TAB_CONS fields
                # implies a modification on model consumer coupling file
                if (_testTab[4] and _csvConfTab[4]) or (_testTab[8] and _csvConfTab[8]) or\
                        (_testTab[9] and _csvConfTab[9]):

                    # if model is not referenced in dictionary => add it
                    if _cnxCSVObj.modoccCons not in _aliasTodoCons.keys():
                        _aliasTodoCons[_cnxCSVObj.modoccCons]=[]

                    # add alias object in tab
                    if _cnxCSVObj.getConsAlias():
                        _aliasTodoCons[_cnxCSVObj.modoccCons].append(_cnxCSVObj.getConsAlias())

                    pass



                # a difference on INIT field
                # implies a modification on initflot file
                if _testTab[5]:
                    pass



                print(_flotObj.compCnx(_cnxCSVObj))
            print('[CSV parser] *************************************************')

    finally:
        file.close()

def getCsvParameterTab(headerTab):

    # set possible header in CSV file
    _possibleField = ['MODOCC_PROD','PORT_PROD','OP_PROD','TAB_PROD',
                      'SIGNAL','INIT',
                      'MODOCC_CONS','PORT_CONS','OP_CONS','TAB_CONS']

    # index tab of mandatory field/header in CSV file
    _mandatoryFieldIndex = [0, 1, 6, 7]

    # output tab initialization
    _configurationTab = []

    for _index, _field in enumerate(_possibleField):
        if _field in headerTab:
            _configurationTab[_index] = True
        else:
            _configurationTab[_index] = False

            # check here if mandatory field is present
            if _index in _mandatoryFieldIndex:
                logger.error(
                    "[CSV HEADER ERROR] CSV file Header must contains at least: MODOCC_PROD;PORT_PROD;MODOCC_CONSO;PORT_CONSUM;")
                return False

    return _configurationTab


def parseCsvLine(DicoLine):

    #
    # key of dictionnary are set with header line of csv file (with csv.DictReader)
    # to test the header line with only test keys of dictionary
    #

    #
    # create a potential connexion object from a tab fill with CSV elements
    #
    tab = [None] * 10

    tab[0] = DicoLine['MODOCC_PROD']
    tab[1] = DicoLine['PORT_PROD']
    tab[6] = DicoLine['MODOCC_CONSO']
    tab[7] = DicoLine['PORT_CONSUM']

    if 'OP_PROD' in DicoLine.keys():
        tab[2] = DicoLine['OP_PROD']

    if 'TAB_PROD' in DicoLine.keys():
        tab[3] = DicoLine['TAB_PROD']

    if 'SIGNAL' in DicoLine.keys():
        tab[4] = DicoLine['SIGNAL']

    if 'INIT' in DicoLine.keys():
        tab[5] = DicoLine['INIT']

    if 'OP_CONS' in DicoLine.keys():
        tab[8] = DicoLine['OP_CONS']

    if 'TAB_CONS' in DicoLine.keys():
        tab[9] = DicoLine['TAB_CONS']

    _cnxObj = PotentialConnexionFromTab(tab)

    return _cnxObj

main()