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
channelEYCNameFlag = False

# force channel renaming flag
forceChannelNameFlag = False

# string to suffix patched signal names
signalPatchString = "_PATCH_MEXINT"


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


                # a difference on one of these fields MODOCC_PROD;PORT_PROD;SIGNAL
                # implies a modification on model producer coupling file
                # and maybe on several other consumer coupling file
                if (_testTab[0] and _csvConfTab[0]) or (_testTab[1] and _csvConfTab[1]) or \
                        (_testTab[4] and _csvConfTab[4]):

                    # compute targetted signal name depending on options
                    _signalTargetObj = computeTargetSignal(_flotObj, _cnxCSVObj, _csvConfTab[4], reader.line_num)

                    # if targetted signal already exist in flow
                    if _signalTargetObj:

                        # we test here if targetted signal is link to targetted producer port in flow
                        # if the same, producer triplet issued from CSV and FLOW must be equal
                        # equality case: nothing to change on producer coupling.
                        # if producer are not the same => there is a patch to be done on other ports
                        # the behavior will depend on forceChannelNameFlag option
                        if _cnxCSVObj.getProdTriplet() != _signalTargetObj.getProducerTriplet():

                            # force channel rename option is activated
                            # we patch signal name for producer and other consumer than current consumer
                            # linked to targetted signal in flow (_signalTargetObj)
                            if forceChannelNameFlag:

                                #
                                # if targetted signal is produced in current flow
                                # we have to patch the alias on it on coupling file to avoid multi produced signals
                                #
                                if _signalTargetObj.getProducerTriplet():

                                    # get current alias on producer port
                                    _aliasProdCurrentFlow = _flotObj.getAliasForPort(
                                                                                _signalTargetObj.getProducerTriplet())

                                    # create a corresponding MEXICO alias object
                                    _aliasProdCurrentFlow = MexicoAlias(_aliasProdCurrentFlow)

                                    # patch alias
                                    _aliasProdCurrentFlow.channel = _aliasProdCurrentFlow.channel+signalPatchString
                                    _aliasProdCurrentFlow.comment = "[MEXICO_INTG] patch signal name"
                                    _aliasProdCurrentFlow.date = displayDate

                                #
                                # treat here the currently linked to targetted channel consummers
                                # we add a patch on coupling (to rename channel) except for current consumer.
                                for _portConsObjCurrentFlow in _signalTargetObj.getConsumerList():

                                    # exclude current consumer i..e consumer from CSV
                                    if _portConsObjCurrentFlow.getIdentifier() == _cnxCSVObj.getConsTriplet():
                                        continue
                                    else:
                                        # get current alias on consumer port
                                        _aliasConsCurrentFlow = _flotObj.getAliasForPort(
                                                                            _portConsObjCurrentFlow.getIdentifier())

                                        # create a corresponding MEXICO alias object
                                        _aliasConsCurrentFlow = MexicoAlias(_aliasConsCurrentFlow)

                                        # patch alias
                                        _aliasConsCurrentFlow.channel = _aliasConsCurrentFlow.channel+signalPatchString
                                        _aliasConsCurrentFlow.comment = "[MEXICO_INTG] patch signal name"
                                        _aliasConsCurrentFlow.date = displayDate

                            # forceChannelNameFlag is not set
                            # channel cannot be modified without impact on other coupling
                            # => signal targetted is maintained to signal link to targetted producer port in current
                            # flow
                            else:

                                # get the targetted producer port object in current flow
                                # (the linked channel name will be used for target signal name)
                                _prodTmpObj = _flotObj.getPort(_cnxCSVObj.getProdTriplet())

                                # warn that targetted signal name could not be reached
                                logger.warning("[CheckCSV][line " + str(
                                    reader.line_num) + "] -- force Channel Name option is not activated --\n\t\t "
                                    "the following signal name: " + _signalTargetObj + " could not be set without "
                                    "modification on other coupling. Channel "+_prodTmpObj.channel+" will be used "
                                                                                    "instead of " + _cnxCSVObj.Channel)

                                # modify the targetted signal name object
                                _signalTargetObj = _flotObj.getChannel(_prodTmpObj.channel)

                        # targetted producer port is already link to targetted signal in current flow
                        # no path to apply no modification on producer alias
                        else:
                            pass
                    # targetted signal doesn't exist in flow
                    # => no other signal to patch
                    # targetted signal will be created by alias on producer port
                    else:


                        pass


                    # modify


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


def computeTargetSignal(_flotObj, _cnxCSVObj, channelIsSpecifiedOnCsv, line_num):

    _TargetProdTriplet = _cnxCSVObj.getProdTriplet()
    _TargetProdTripletObjInFlow = _flotObj.getPort(_TargetProdTriplet)

    if not channelEYCNameFlag:
        if channelIsSpecifiedOnCsv:
            _TargetSignal = _cnxCSVObj.Channel
        else:
            _TargetSignal = _TargetProdTripletObjInFlow.channel
    else:
        _signalNameEYC = _TargetProdTripletObjInFlow.name
        _signalNameEYC += "_"
        _signalNameEYC += _TargetProdTripletObjInFlow.channel
        _signalNameEYC = _signalNameEYC.replace("/", "_")
        if _cnxCSVObj.Channel != _signalNameEYC:
            logger.warning("[CheckCSV][line " + str(line_num) + "] -- EYC channel name option activated --\n\t\t "
                                                            "the following signal name: "+_signalNameEYC+" will be "
                                                            "used instead of "+_cnxCSVObj.Channel)
        _TargetSignal = _signalNameEYC

    return _flotObj.getChannel(_TargetSignal)

def getCsvParameterTab(headerTab):

    # set possible header in CSV file
    _possibleField = ['MODOCC_PROD','PORT_PROD','OP_PROD','TAB_PROD',
                      'SIGNAL','INIT',
                      'MODOCC_CONS','PORT_CONS','OP_CONS','TAB_CONS']

    # index tab of mandatory field/header in CSV file
    _mandatoryFieldIndex = [0, 1, 6, 7]

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