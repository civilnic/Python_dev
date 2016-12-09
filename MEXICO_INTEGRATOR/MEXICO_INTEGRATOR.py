import sys
import csv
import logging
from logging.handlers import RotatingFileHandler,BaseRotatingHandler
from datetime import datetime

from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig
from FLOT.connexion import PotentialConnexionFromTab
from FLOT.flot import flot
from FLOT.alias import Alias,MexicoAlias

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

# EYC channel naming rules flag
channelEYCNameFlag = True

# force channel renaming flag
forceChannelNameFlag = True

# string to suffix patched signal names
signalPatchString = "_PATCH_MEXINT"

# set possible header in CSV file
_possibleField = ['MODOCC_PROD', 'PORT_PROD', 'OP_PROD', 'TAB_PROD',
                  'SIGNAL', 'INIT',
                  'MODOCC_CONS', 'PORT_CONS', 'OP_CONS', 'TAB_CONS']

# CSV current line for logger
line_num = 0

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
    parser = OptionParser("usage: %prog --csv <csvFile> --mexico <mexicoCfgFile> --cp <mexicoconceptionFile>")
    parser.add_option("--csv", dest="csvFile", help="CSV file containing connexions/inits to integer",
                      type="string", metavar="FILE")
    parser.add_option("--mexico", dest="mexicoCfgFile", help="Mexico configuration file (.xml)",
                      type="string", metavar="FILE")
    parser.add_option("--cp", dest="mexicoConceptionFile", help="Mexico conception file (.xml)",
                      type="string", metavar="FILE")
    (options, args) = parser.parse_args()

    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _csvFile = options.csvFile
    _mexicoCfgFile = options.mexicoCfgFile
    _conceptionFile = options.mexicoConceptionFile


    logger.info("_csvFile: "+_csvFile)
    logger.info("_mexicoCfgFile: "+_mexicoCfgFile)
    logger.info("_conceptionFile: "+_conceptionFile)

    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(_mexicoCfgFile)
    _mexicoCfgObj.conceptionFile = _conceptionFile

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

    #
    # dictionary of alias modification to do per model
    #
    _aliasTodoCons = {}
    _aliasTodoProd = {}

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

            # line number global variable set for logger in other function
            line_num = reader.line_num

            # if channelEYCNameFlag is True we have to take into account channel name differences
            if channelEYCNameFlag:
                _csvConfTab[4] = True

            # differences analysis and translation in term of aliases on modele/port
            if _testTab != [False] * 10:

                # a difference on MOD_CONS or PORT_CONS is not possible
                # due to the cnxObj comparison nature (it construct from the same
                # MOD_CONS and PROD_CONS)
                if (_testTab[6] and _csvConfTab[6]) or (_testTab[7] and _csvConfTab[7]):
                    logger.error("[CheckCSV][line " + str(reader.line_num) + "] -- ERROR on Treatment: this case is"
                                                                             "not possible --")
                    continue


                # a difference on one of these fields MODOCC_PROD;PORT_PROD;SIGNAL
                # implies a modification on model producer coupling file
                # and maybe on several other consumer coupling file

                if (_testTab[0] and _csvConfTab[0]) or (_testTab[1] and _csvConfTab[1]) or \
                        (_testTab[4] and _csvConfTab[4]):

                    #
                    # No producer model and/or port has been set on CSV
                    # it could be :
                    #       a dcnx
                    #       an simple initialization
                    #       a aliaa on signal
                    if _cnxCSVObj.getProdTriplet() is None:
                        print(_csvConfTab)
                        #
                        # if SIGNAL column is present in CSV
                        # its a simple initialization and/or an alias
                        # this test not use _csvConfTab[4] because it can be forced to TRUE with EYC name option
                        if _possibleField[4] in row.keys():

                            # if S_USER from CSV if not None
                            # It's a simple alias case
                            if row[_possibleField[4]]:
                                print (_cnxCSVObj.modoccCons)
                                print (_cnxCSVObj.Channel)

                                # check S_USER existence in flow


                        # S_USER is not specified
                        # => it a DCNX
                        else:
                                pass



                    pass


            #(_flotObj.compCnx(_cnxCSVObj))
            #print('[CSV parser] *************************************************')

    finally:
        file.close()

    print ("**** ALIAS PROD ****")
    for modele in _aliasTodoProd.keys():
        print('modele: ' + modele)
        if _aliasTodoProd[modele]:
            for port in _aliasTodoProd[modele].keys():
                print('port: ' + port)
                print(_aliasTodoProd[modele][port])
            pass

    print("**** ALIAS CONSO ****")
    for modele in _aliasTodoCons.keys():
        print('modele: ' + modele)
        if _aliasTodoCons[modele]:
            for port in _aliasTodoCons[modele].keys():
                print('port: ' + port)
                print(_aliasTodoCons[modele][port])
            pass

# fill dictionary of coupling to be done from alias object
# to sort coupling by model

def ListCouplingToBeDone(aliasObj, portObj, dictCpl):

    global logger,line_num

    # test if model assoicate to port is alreday in coupling dict
    # else create an empty dict for model key
    if portObj.modocc not in dictCpl.keys():
        dictCpl[portObj.modocc] = dict()

    # test port key in dictionary for model
    # if no aliases is specifed on
    if portObj.name not in dictCpl[portObj.modocc].keys():
        dictCpl[portObj.modocc][portObj.name] = aliasObj

    # an alias exist for model/port in "alias to be done" dictionary
    # check if it's the same coupling or not
    # if not raise an CSV error
    # else it 's a warning on CSV content
    else:
        # compare alias object
        if aliasObj != dictCpl[portObj.modocc][portObj.name]:
            logger.warning("[CheckCSV][line " + str(line_num) + "] -- Different connection specified for port: "
                           + portObj.getIdentifier + "--\n\t\t ")


# function to return the corresponding Signal name following EYC rule: portName_modelname_modeloccurence
# it constructed from a portObj
def computeEYCname(portObj):

    _signalNameEYC = portObj.name
    _signalNameEYC += "_"
    _signalNameEYC += portObj.modocc
    _signalNameEYC = _signalNameEYC.replace("/", "_")

    return _signalNameEYC

def computeTargetSignal(_flotObj, _cnxCSVObj, channelIsSpecifiedOnCsv):

    global logger,line_num

    _TargetProdTriplet = _cnxCSVObj.getProdTriplet()
    _TargetProdTripletObjInFlow = _flotObj.getPort(_TargetProdTriplet)

    if not channelEYCNameFlag:

        if channelIsSpecifiedOnCsv:
            _TargetSignal = _cnxCSVObj.Channel
        else:
            _TargetSignal = _TargetProdTripletObjInFlow.channel

    else:
        _signalNameEYC = computeEYCname(_TargetProdTripletObjInFlow)

        if _cnxCSVObj.Channel != _signalNameEYC:
            logger.warning("[CheckCSV][line " + str(line_num) + "] -- EYC channel name option activated --\n\t\t "
                                                            "the following signal name: "+_signalNameEYC+" will be "
                                                            "used instead of "+_cnxCSVObj.Channel)
        _TargetSignal = _signalNameEYC

    return _TargetSignal

def getCsvParameterTab(headerTab):

    global _possibleField

    # index tab of mandatory field/header in CSV file
    _mandatoryFieldIndex = [6, 7]

    # output tab initialization
    _configurationTab = [False]*10

    for _index, _field in enumerate(_possibleField):

        if _field in headerTab:
            _configurationTab[_index] = True
        else:
            _configurationTab[_index] = False

            # check here if mandatory field is present
            if _index in _mandatoryFieldIndex:
                global logger
                logger.error(
                    "\n[CSV HEADER ERROR] CSV file Header must contains at least:"
                    +_possibleField[0]+";"+_possibleField[1]+";"+_possibleField[6]+";"+_possibleField[7]+";")
                logger.error("[CSV HEADER ERROR] Missing: "+_possibleField[_index])
                sys.exit(1)

    return _configurationTab


def parseCsvLine(DicoLine):

    global _possibleField

    #
    # key of dictionnary are set with header line of csv file (with csv.DictReader)
    # to test the header line with only test keys of dictionary
    #

    #
    # create a potential connexion object from a tab fill with CSV elements
    #
    tab = [None] * 10

    if _possibleField[0] in DicoLine.keys():
        tab[0] = DicoLine[_possibleField[0]]
    if _possibleField[1] in DicoLine.keys():
        tab[1] = DicoLine[_possibleField[1]]

    tab[6] = DicoLine[_possibleField[6]]
    tab[7] = DicoLine[_possibleField[7]]

    if _possibleField[2] in DicoLine.keys():
        tab[2] = DicoLine[_possibleField[2]]

    if _possibleField[3] in DicoLine.keys():
        tab[3] = DicoLine[_possibleField[3]]

    if _possibleField[4] in DicoLine.keys():
        tab[4] = DicoLine[_possibleField[4]]

    if _possibleField[5] in DicoLine.keys():
        tab[5] = DicoLine[_possibleField[5]]

    if _possibleField[8] in DicoLine.keys():
        tab[8] = DicoLine[_possibleField[8]]

    if _possibleField[9] in DicoLine.keys():
        tab[9] = DicoLine[_possibleField[9]]

    _cnxObj = PotentialConnexionFromTab(tab)

    return _cnxObj

main()