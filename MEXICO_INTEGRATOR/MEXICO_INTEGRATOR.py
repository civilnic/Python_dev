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

# EYC channel naming rules flag
channelEYCNameFlag = True

# force channel renaming flag
forceChannelNameFlag = False

# force initialization flag (to force intiialization in conflict cases)
forceInitFlag = False

# string to suffix patched signal names
signalPatchString = "_PATCH_MEXINT"

# set possible header in CSV file
_possibleField = ['MODOCC_PROD', 'PORT_PROD', 'OP_PROD', 'TAB_PROD',
                  'SIGNAL', 'INIT',
                  'MODOCC_CONS', 'PORT_CONS', 'OP_CONS', 'TAB_CONS']

# CSV current line for logger
line_num = 0

# comment to add in coupling/init files
globalComment = ""

#
# dictionary of alias modification to do per model
#
_aliasConsDict = {}
_aliasProdDict = {}
_initializationDict = {}
_initializationDictPerModel = {}

_mexicoCfgObj = None


def main():

    global _mexicoCfgObj, globalComment, channelEYCNameFlag, forceChannelNameFlag, forceInitFlag

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
    parser.add_option("--cmt", dest="Comment", help="Comment to add in coupling and init files",
                      type="string")
    parser.add_option("--eyc", dest="eycName", action="store_true", help="EYC channel naming rules flag")
    parser.add_option("--fs", dest="forceSignal", action="store_true",
                      help="in case of conflict: force channel renaming flag")
    parser.add_option("--fi", dest="forceInit", action="store_true",
                      help="in case of conflict: force initialization")
    (options, args) = parser.parse_args()

    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _csvFile = options.csvFile
    _mexicoCfgFile = options.mexicoCfgFile
    _conceptionFile = options.mexicoConceptionFile
    globalComment = options.Comment
    channelEYCNameFlag = options.eycName
    forceChannelNameFlag = options.forceSignal
    forceInitFlag = options.forceInit

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

    # parse MEXICO flow file
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

    global _mexicoCfgObj, globalComment

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

                # get compared consumer port from flow
                _consPortObj = _flotObj.getPort(_cnxCSVObj.getConsTriplet())

                # S_FLOW = channel link to consummer port in flow
                S_FLOW = _consPortObj.channel.name
                S_FLOWObj = _flotObj.getChannel(S_FLOW)

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

                    # if connexion is modified we force operator / tab differences to evaluate them
                    _testTab[8] = True
                    _testTab[9] = True

                    #
                    # No producer model and/or port has been set on CSV
                    # it could be :
                    #       a dcnx
                    #       an simple initialization
                    #       a aliaa on signal
                    if _cnxCSVObj.getProdTriplet() is None:

                        #
                        # if SIGNAL column is present in CSV
                        # its a simple initialization and/or an alias
                        # this test not use _csvConfTab[4] because it can be forced to TRUE with EYC name option
                        if _possibleField[4] in row.keys():

                            # if S_USER from CSV is not None
                            # It's a simple alias case
                            if _cnxCSVObj.Channel:

                                # check S_USER existence in flow
                                S_USER = _cnxCSVObj.Channel

                                # create an alias on S_USER for consumer port
                                _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                    index=_cnxCSVObj.tabCons,
                                                                    operator=_cnxCSVObj.operatorCons,
                                                                    comment=globalComment, date=displayDate)

                                # add it in Alias dictonary
                                AddAlias(_TargetConsummerAlias, _consPortObj)

                                # Apply init algorithm
                                AlgoInits(_flotObj,_cnxCSVObj)

                        # S_USER is not specified
                        # => it a DCNX
                        else:

                            pass
                           # if S_FLOW != _cnxCSVObj.portCons:

                                # create an alias on S_USER for consumer port
                           #     _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons,
                           #                                         channel=_cnxCSVObj.portCons,
                           #                                         index=_cnxCSVObj.tabCons,
                           #                                         operator=_cnxCSVObj.operatorCons,
                           #                                         comment=globalComment, date=displayDate)

                                # add it in Alias dictonary
                           #     AddAlias(_TargetConsummerAlias, _consPortObj)

                           # else:

                                # create an alias on S_USER for consumer port
                           #     _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_FLOW+"_DCNX",
                           #                                         index=_cnxCSVObj.tabCons,
                           #                                         operator=_cnxCSVObj.operatorCons,
                           #                                         comment=globalComment, date=displayDate)

                                # add it in Alias dictonary
                           #     AddAlias(_TargetConsummerAlias, _consPortObj)

                            # Apply init algorithm
                           # AlgoInits(_flotObj, _cnxCSVObj, True)


                    # a model/port producer is speficied in CSV
                    else:

                        # producer port object linked to target producer port (from CSV)
                        _prodPortObj = _flotObj.getPort(_cnxCSVObj.getProdTriplet())


                        # if SIGNAL column is present in CSV
                        # its a simple initialization and/or an alias
                        # this test not use _csvConfTab[4] because it can be forced to TRUE with EYC name option
                        # IF EYC option is activated S_USER = S_EYC
                        if channelEYCNameFlag:
                            S_USER = computeEYCname(_prodPortObj)
                        # else S_USER = S_CSV
                        elif _possibleField[4] in row.keys():
                            S_USER = _cnxCSVObj.Channel
                        # else S_USER = S_FLOW
                        else:
                            S_USER = _prodPortObj.channel.name

                        #  channel object link to specified signal name in flow
                        _channelObj = _flotObj.getChannel(S_USER)

                        # if S_USER exist in flow
                        if _channelObj:

                            # if S_USER is produced
                            if _channelObj.getProducer():

                                # if S_USER is link to targeted producer port (i.e port specified on CSV)
                                if _channelObj.getProducer().getIdentifier() == _cnxCSVObj.getProdTriplet():

                                    # create an alias on S_USER for consumer port
                                    _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                        index=_cnxCSVObj.tabCons,
                                                                        operator=_cnxCSVObj.operatorCons,
                                                                        comment=globalComment, date=displayDate)
                                    #
                                    # ________test_________
                                    #
                                    if _cnxCSVObj.operatorCons:
                                        _TargetConsummerAlias.operator = _cnxCSVObj.operatorCons

                                    if _cnxCSVObj.tabCons:
                                        _TargetConsummerAlias.index = _cnxCSVObj.tabCons

                                    # add it in Alias dictionary
                                    AddAlias(_TargetConsummerAlias, _consPortObj)

                                    # apply algo inits
                                    AlgoInits(_flotObj, _cnxCSVObj)

                                # producer port link to S_USER in flow is not the one specified in CSV file
                                else:

                                    # if force channel option is activated => we want to rename previous S_USER in flow
                                    if forceChannelNameFlag:

                                        # get producer port linked to S_USER in flow
                                        _prodPortToPatchObj = _channelObj.getProducer()

                                        if len(_channelObj.getConsumerList()) == 0 \
                                                and ((computeEYCname(_prodPortToPatchObj) != S_USER)
                                                     or (_prodPortToPatchObj != S_USER)):

                                            if channelEYCNameFlag:

                                                # create an alias with EYC rule name
                                                _TargetAlias = MexicoAlias(port=_prodPortToPatchObj.name,
                                                                           channel=computeEYCname(_prodPortToPatchObj),
                                                                           index=_prodPortToPatchObj.index,
                                                                           operator=_prodPortToPatchObj.operator,
                                                                           comment=globalComment, date=displayDate)

                                                # add it in Alias dictionary
                                                AddAlias(_TargetAlias, _prodPortToPatchObj)

                                            else:
                                                # create an alias on producer port name (equiv. to no alias)
                                                _TargetAlias = MexicoAlias(port=_prodPortToPatchObj.name,
                                                                           channel=_prodPortToPatchObj.name,
                                                                           index=_prodPortToPatchObj.index,
                                                                           operator=_prodPortToPatchObj.operator,
                                                                           comment=globalComment, date=displayDate)

                                                # add it in Alias dictionary
                                                AddAlias(_TargetAlias, _prodPortToPatchObj)

                                        # patch S_USER in flow
                                        else:

                                            # create patch aliases on port linked to S_USER in flow
                                            _patchName = RenameChannel(_flotObj, S_USER, _cnxCSVObj, False, True)

                                            logger.warning(
                                                "[CheckCSV][line " + str(line_num) + "] Force Channel option is ON\n"
                                                " -- Channel " + S_USER + " has been renamed into  " + _patchName)

                                            # if channel renamed has an init, we have set it into channel new name
                                            if _channelObj.init:

                                                # create a fake copy of channel object and set name with patch name
                                                _channelObjPatched = copy.copy(_channelObj)
                                                _channelObjPatched.name = _patchName

                                                # if an initialization was set on S_USER transfert it to the new S_USER
                                                # patch signal
                                                AddInit(_channelObjPatched, _channelObjPatched.getProducer())

                                                logger.warning(
                                                    "[CheckCSV][line " + str(line_num) + "] Force Channel option is ON\n"
                                                    " -- Initialization " + _patchName +
                                                    " has been renamed to  " + _channelObjPatched.init)

                                        # create patch aliases on port linked to S_USER in flow
                                        RenameChannel(_flotObj, S_USER, _cnxCSVObj, True, False)

                                        # create an alias on S_USER for consumer port
                                        _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                            index=_cnxCSVObj.tabCons,
                                                                            operator=_cnxCSVObj.operatorCons,
                                                                            comment=globalComment, date=displayDate)


                                        # add it in Alias dictionary
                                        AddAlias(_TargetConsummerAlias, _consPortObj)

                                        # apply algo inits
                                        AlgoInits(_flotObj, _cnxCSVObj)

                                    else:

                                        S_USER = _prodPortObj.channel.name

                                        # create an alias on S_USER for consumer port
                                        _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                            index=_cnxCSVObj.tabCons,
                                                                            operator=_cnxCSVObj.operatorCons,
                                                                            comment=globalComment, date=displayDate)

                                        # add it in Alias dictionary
                                        AddAlias(_TargetConsummerAlias, _consPortObj)

                                        # apply algo inits
                                        AlgoInits(_flotObj, _cnxCSVObj)

                            # S_USER exists in flow but is not produced:
                            else:

                                # create an alias on S_USER for producer port
                                _TargetProducerAlias = MexicoAlias(port=_cnxCSVObj.portProd, channel=S_USER,
                                                                    index=_cnxCSVObj.tabProd,
                                                                    operator=_cnxCSVObj.operatorProd,
                                                                    comment=globalComment, date=displayDate)

                                # add it in Alias dictionary
                                AddAlias(_TargetProducerAlias, _prodPortObj)


                                # create an alias on S_USER for consumer port
                                _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                    index=_cnxCSVObj.tabCons,
                                                                    operator=_cnxCSVObj.operatorCons,
                                                                    comment=globalComment, date=displayDate)

                                # add it in Alias dictionary
                                AddAlias(_TargetConsummerAlias, _consPortObj)

                                # apply algo inits
                                AlgoInits(_flotObj, _cnxCSVObj)


                        # S_USER not exists in flow
                        else:

                            # create patch aliases on port linked to S_USER in flow
                            RenameChannel(_flotObj, S_USER, _cnxCSVObj, True, False)

                            # create an alias on S_USER for consumer port
                            _TargetConsummerAlias = MexicoAlias(port=_cnxCSVObj.portCons, channel=S_USER,
                                                                index=_cnxCSVObj.tabCons,
                                                                operator=_cnxCSVObj.operatorCons,
                                                                comment=globalComment, date=displayDate)
                            # add it in Alias dictionary
                            AddAlias(_TargetConsummerAlias, _consPortObj)

                            # apply algo inits
                            AlgoInits(_flotObj, _cnxCSVObj)

                if ((_testTab[8] and _csvConfTab[8])) or ((_testTab[9] and _csvConfTab[9])):

                    if _cnxCSVObj.modoccCons in _aliasConsDict.keys():

                       if _cnxCSVObj.portCons in _aliasConsDict[_cnxCSVObj.modoccCons]:
                            _prevaliasObject = _aliasConsDict[_cnxCSVObj.modoccCons][_cnxCSVObj.portCons]
                            _aliasObject = copy.copy(_prevaliasObject)

                            del _aliasConsDict[_cnxCSVObj.modoccCons][_cnxCSVObj.portCons]

                       else:
                            # create an alias on S_USER for consumer port
                            _aliasObject = MexicoAlias( port=_cnxCSVObj.portCons, channel=_cnxCSVObj.Channel,
                                                        operator=_cnxCSVObj.operatorCons,
                                                        comment=globalComment, date=displayDate)

                       # add it in Alias dictionary
                       AddAlias(_aliasObject, _consPortObj)

                    else:
                        # create an alias on S_USER for consumer port
                        _aliasObject = MexicoAlias(port=_cnxCSVObj.portCons, channel=_cnxCSVObj.Channel,
                                                   operator=_cnxCSVObj.operatorCons,
                                                   comment=globalComment, date=displayDate)

                        # add it in Alias dictionary
                        AddAlias(_aliasObject, _consPortObj)

                if ((_testTab[5] and _csvConfTab[5])):

                    if ((_testTab[4] and _csvConfTab[4]) and not channelEYCNameFlag):
                        AlgoInits(_flotObj, _cnxCSVObj)
                    else:
                        _cnxCSVObj.Channel = _consPortObj.channel.name
                        AlgoInits(_flotObj, _cnxCSVObj)

    finally:
        file.close()

    logger.info("**** ALIAS PROD ****")
    for modele in _aliasProdDict.keys():

        actorObj = _mexicoCfgObj.getActor(modele)

        _coulingFileObj = mexico_coupling(actorObj.getFirstCplFile())

        logger.info("modele: "+modele)

        if _aliasProdDict[modele]:

            for port in sorted(_aliasProdDict[modele].keys()):
               # logger.info("port: " + port)
                #logger.info("alias:")
               # logger.info(_aliasProdDict[modele][port])

                _coulingFileObj.chgAddModify(_aliasProdDict[modele][port], "FUN_OUT")

        _coulingFileObj.write()

    logger.info("**** ALIAS CONSO ****")
    for modele in _aliasConsDict.keys():

        actorObj = _mexicoCfgObj.getActor(modele)

        _coulingFileObj = mexico_coupling(actorObj.getFirstCplFile())

        logger.info("modele: "+modele)

        if _aliasConsDict[modele]:

            for port in sorted(_aliasConsDict[modele].keys()):

               # logger.info("port: " + port)
              #  logger.info("alias: ")
               # logger.info(_aliasConsDict[modele][port])

                _coulingFileObj.chgAddModify(_aliasConsDict[modele][port], "FUN_IN")

        logger.info("update coupling file: " + _coulingFileObj.pathname)
        _coulingFileObj.write()


    logger.info("**** INITS ****")
    #
    # get Init MICD from MEXICO configuration file
    #
    _initFile = _mexicoCfgObj.getInitFilePathName()

    if _initFile:

        if len(_initializationDictPerModel.keys()) > 0:

            logger.info(" MEXICO Init file updated: " + _initFile)

            # Parse init file and create MICD object
            _MICD_Inits = Mexico_Init_File(_initFile)

            # Initializations are stored by mod/occ in _initializationDictPerModel dictionary
            # to read only one time each MICD
            for _modocc in sorted(_initializationDictPerModel.keys()):

                _currentMICD = None
                _micdObj = None

                # each initialization is then stored by consumer port object
                for _portObj in _initializationDictPerModel[_modocc].keys():

                    # get relative channel object in Mexico flow
                    _channelObj = _initializationDictPerModel[_modocc][_portObj]

                    logger.info("\tChannel treated: " + _channelObj.name)

                    # if channel already set in init file
                    # try to get MICD port Obj (i.e. the line corresponding to channel in Initialization MICD)
                    _MICDPortObj = _MICD_Inits.getPortObj(_channelObj.name)

                    # If _MICDPortObj is not None that means that channel is already initialized in Init file.
                    # we have to test the initialized value and change it if different
                    if _MICDPortObj:
                        logger.info("\t\t --> Channel is initialized in initfile")

                        # if targetted init is None => Init to remove
                        if _channelObj.init is None:
                            logger.info("\t\t\t init is None => remove from init file")

                            # add init port to initFile
                            _MICD_Inits.RemovePortfromPortObject(_MICDPortObj, "FUN_OUT")

                            continue

                        #
                        # test set value
                        # if value is not the same that targeted value change it in Init file
                        #
                        try:
                            # if channel
                            if (_MICDPortObj.initdefaultvalue is not None) and (_channelObj.init is not None):
                                if float(_MICDPortObj.initdefaultvalue) == float(_channelObj.init):
                                    logger.info("\t\t\tEquivalent initialization is already set in init file: "+_MICDPortObj.initdefaultvalue)
                                    logger.info("\t\t\tinit required in csv: "+_channelObj.init)
                                    logger.info("\t\t\t=> nothing to do for this channel ")
                                    continue
                        except ValueError:
                            pass

                        if _MICDPortObj.initdefaultvalue != _channelObj.init:

                            logger.info("\t\t\tChannel was previously initialized to: " + _MICDPortObj.initdefaultvalue)
                            logger.info("\t\t\tand is modified to: " + _channelObj.init)

                            # change init value
                            _MICDPortObj.initdefaultvalue = _channelObj.init

                            # add modification comment in init file (in description field)
                            _MICDPortObj.description = globalComment

                            # add init port to initFile
                            _MICD_Inits.AddPortfromPortObject(_MICDPortObj, "FUN_OUT")

                        else:
                            logger.info("\t\t\tChannel is already initialized in flot to: " + _channelObj.init)

                    # channel is not defined in init file
                    else:
                        logger.info("\t\t --> Channel is not initialized in initfile")
                        #
                        _mexChannelObj = _flotObj.getChannel(_channelObj.getIdentifier())
                        if _mexChannelObj:
                            if _mexChannelObj.init:

                                logger.info("\t\t\tIn MEXICO flot Channel is initialized to: "+_mexChannelObj.init)

                                try:
                                    if (_mexChannelObj.init is not None) and (_channelObj.init is not None):
                                        if float(_mexChannelObj.init) == float(_channelObj.init):
                                            logger.info("\t\t\tEquivalent initialization is already set in flot (from MICD): " + _mexChannelObj.init)
                                            logger.info("\t\t\tinit required in csv: " + _channelObj.init)
                                            logger.info("\t\t\t=> nothing to do for this channel: ")
                                            continue
                                        if float(_mexChannelObj.init) != float(_channelObj.init):
                                            logger.info("\t\t\tinit required in csv: " + _channelObj.init)
                                            logger.info("\t\t\t=> apply for this channel: " + _channelObj.init)
                                            break
                                    if _channelObj.init is not None:
                                        # if channel init is set to 0 => do not add into InitFile
                                        if float(_channelObj.init) == 0.0:
                                            logger.info("\t\t\tSpecified init not added (null initialization): " + _channelObj.init)
                                            continue

                                except ValueError:

                                    if _mexChannelObj.init == _channelObj.init:
                                        logger.info("\t\t\tEquivalent initialization is already set in flot (from MICD): " + _mexChannelObj.init)
                                        logger.info("\t\t\tinit required in csv: " + _channelObj.init)
                                        logger.info("\t\t\t=> nothing to do for this channel: ")
                            else:
                                logger.info("\t\t\tChannel is not initialized in MEXICO flot")
                        else:
                            logger.info("\t\t\tChannel didn't exist in MEXICO flot")

                        # get actor corresponding to modocc in Mexico configuration
                        _actorObj = _mexicoCfgObj.getActor(_modocc)

                        # list micd corresponding to current actor in Mexico configuration
                        # for each micd
                        for _micd in _actorObj.getMICDList():

                            if ((_currentMICD is None) or (_currentMICD != _micd._fullPathName)):
                                _currentMICD = _micd._fullPathName

                            if _micdObj is None:
                                # create micd object (i.e. parse MICD) from MICD
                                _micdObj = MICD(_micd._fullPathName)

                            # get an MicdPort Object for consumer port
                            _consPortObj = _micdObj.getPortObj(_portObj.name)

                            # if this object is not None => consumer has been found on MICD
                            # get needed informations from MICD line
                            if _consPortObj:

                                # create a new MICD Port object to add in init file
                                # this port will correspond to channel to add in init file

                                _initPort = INIT_port(None, "OUT", None)

                                _initPort.name = _channelObj.name
                                _initPort.codingtype = _consPortObj.codingtype
                                _initPort.unit = _consPortObj.unit
                                _initPort.description = globalComment
                                _initPort.convention = _consPortObj.convention
                                _initPort.dim1 = _consPortObj.dim1
                                _initPort.dim2 = _consPortObj.dim2
                                _initPort.comformat = _consPortObj.comformat
                                _initPort.fromto = _consPortObj.fromto
                                _initPort.min = _consPortObj.min
                                _initPort.max = _consPortObj.max
                                _initPort.initdefaultvalue = _channelObj.init

                                # add init port to initFile
                                _MICD_Inits.AddPortfromPortObject(_initPort, "FUN_OUT")

                                logger.info("\t\tNew channel is added to init file, value set to: " + _channelObj.init)

                                break

            _MICD_Inits.savefile()
        else:
            logger.info("No init to update")
    else:
        #
        # log an error
        #
        pass

def RenameChannel(flotObj,channel,cnxCSVObj,fromPROD=True,patchDCNX=False):


    # if fromCSV is true producer port to patch is identified from the cnxCSVObj
    if fromPROD:
        # get port object in flow
        _prodPortObj = flotObj.getPort(cnxCSVObj.getProdTriplet())
    # else the producer is identified from channel name in flow
    else:
        _channelObj = flotObj.getChannel(channel)
        _prodPortObj = _channelObj.getProducer()

    # if this option is set, suffix "_PATCH_MEX_INT" is added to signal name
    if patchDCNX:
        channel = channel + "_PATCH_MEX_INT"



    # create an alias on channel for producer port
    _TargetProducerAlias = MexicoAlias(port=_prodPortObj.name, channel=channel,
                                       index=_prodPortObj.index, operator=_prodPortObj.operator)

    # add alias into alias table
    AddAlias(_TargetProducerAlias,_prodPortObj)

    # channel object link to producer port
    _channelObj = flotObj.getChannel(_prodPortObj.channel.name)

    # list of consumer port object
    _consList = _channelObj.getConsumerList()

    # if channel is consumed
    if _consList:

        # for each consumer port object
        for _consPortObj in _consList:

            # create an alias on channel for producer port
            _ConsumedAlias = MexicoAlias(port=_consPortObj.name, channel=channel,
                                               index=_consPortObj.index, operator=_consPortObj.operator)

            # add alias into alias table
            AddAlias(_ConsumedAlias, _consPortObj)

    return channel


def AlgoInits(flotObj,cnxCSVObj,specSignalName=False):

    # get compared consumer port from flow
    _consPortObj = flotObj.getPort(cnxCSVObj.getConsTriplet())

    # S_FLOW = channel link to consummer port in flow
    S_FLOW = _consPortObj.channel.name
    S_FLOWObj = flotObj.getChannel(S_FLOW)

    if specSignalName:
        S_USER = S_FLOW + "_DCNX"
    else:
        S_USER = cnxCSVObj.Channel



    # IF S_USER not exist in flow
    if flotObj.getChannel(S_USER) is None:

        # create a channel object for S_USER
        S_USERObj = channel(S_USER)

        # link it consumer port
        S_USERObj.addPort(_consPortObj)


        # IF USER_INIT is not None, apply it on the new signal S_USER
        if cnxCSVObj.init:

            # add the initialization value
            S_USERObj.init = cnxCSVObj.init

            # add to inits dictionary
            AddInit(S_USERObj, _consPortObj)

        # USER_INIT is not specified
        else:

            # previous channel on flow has an initialization set ?
            if S_FLOWObj.init:

                # add the initialization value
                S_USERObj.init = S_FLOWObj.init

                # add to inits dictionary
                AddInit(S_USERObj, _consPortObj)

    # S_USER exist in flow
    else:

        # get S_USER channel object
        S_USERObj = copy.copy(flotObj.getChannel(S_USER))

        # IF USER_INIT is not None, apply it on the new signal S_USER
        if cnxCSVObj.init:

            # S_USER channel has no initialization on flow
            if S_USERObj.init is None:

                # add the initialization value
                S_USERObj.init = cnxCSVObj.init

                # add to inits dictionary
                AddInit(S_USERObj, _consPortObj)

                # print a warning message if there is several consumer ports
                if len(S_USERObj.getConsumerList())>1:

                    logger.warning(
                    "[CheckCSV][line " + str(line_num) + "] -- Channel "+S_USER+"is consummed by other model/ports than "+
                    cnxCSVObj.getConsTriplet()+" modify initialization to :"+S_USERObj.init+" could have an impact on them")

            # S_USER channel has an initialization on flow
            else:

                # if init from flow is not the init required in CSV
                if S_USERObj.init != cnxCSVObj.init:

                    # force init option is enabled
                    if forceInitFlag:

                        # add the initialization value
                        S_USERObj.init = cnxCSVObj.init

                        # add to inits dictionary
                        AddInit(S_USERObj, _consPortObj)

                        # print a warning message if there is several consumer ports
                        if len(S_USERObj.getConsumerList()) > 1:
                            logger.warning(
                                "[CheckCSV][line " + str(
                                line_num) + "] -- Channel " + S_USER + "is consummed by other model/ports than " +
                                cnxCSVObj.getConsTriplet() + " modify initialization to :" + S_USERObj.init + " could have an impact on them")

                    # no option to force initialization
                    else:
                        logger.error(
                            "[CheckCSV][line " + str(
                            line_num) + "] -- Channel " + S_USER + " init from CSV "+cnxCSVObj.init +" could not be set !\n"
                            "This channel already have an init: "+S_USERObj.init+"\n")

# fill dictionary of init to be done
# sort init by model

def AddInit(channelObj, portObj):

    # target dictionary
    _dict = _initializationDict

    # test if model assoicate to port is alreday in init dict
    # else create an empty dict for model key
    if channelObj.name not in _dict.keys():
        _dict[channelObj.name] = channelObj
        if portObj.modocc not in _initializationDictPerModel.keys():
            _initializationDictPerModel[portObj.modocc] = {}

        _initializationDictPerModel[portObj.modocc][portObj] = channelObj
    else:

        if channelObj.init != _dict[channelObj.name].init:

            logger.warning("[CheckCSV][line " + str(line_num) + "] -- Several initializations specified for port: "
                           + portObj.getIdentifier() + "--\n\t\tCannot set init: "+str(channelObj.init)+" because it as "
                            "already set to: "+_dict[channelObj.name].init)
        else:
            pass
            #logger.warning("[CheckCSV][line " + str(line_num) + "] -- Several initializations of same value specified "
            #              "for port: "+ portObj.getIdentifier()+ "--\n\t\t")

# fill dictionary of coupling to be done from alias object
# to sort coupling by model

def AddAlias(aliasObj, portObj):

    global logger, line_num, _aliasCons, _aliasProd

    #
    # set target dictionary
    #
    if portObj.type == "consumer":
        _dict = _aliasConsDict
    else:
        _dict = _aliasProdDict

    # test if model assoicate to port is alreday in coupling dict
    # else create an empty dict for model key
    if portObj.modocc not in _dict.keys():
        _dict[portObj.modocc] = dict()

    # test port key in dictionary for model
    # if no aliases is specifed on
    if portObj.name not in _dict[portObj.modocc].keys():
        _dict[portObj.modocc][portObj.name] = aliasObj

    # an alias exist for model/port in "alias to be done" dictionary
    # check if it's the same coupling or not
    # if not raise an CSV error
    # else it 's a warning on CSV content
    else:
        # compare alias object
        if aliasObj != _dict[portObj.modocc][portObj.name]:
            logger.warning("[CheckCSV][line " + str(line_num) + "] -- Several connections specified for port: "
                           + portObj.getIdentifier() + "--\n\t\t ")


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
        if DicoLine[_possibleField[0]]:
            tab[0] = DicoLine[_possibleField[0]]
    if _possibleField[1] in DicoLine.keys():
        if DicoLine[_possibleField[1]]:
            tab[1] = DicoLine[_possibleField[1]]

    tab[6] = DicoLine[_possibleField[6]]
    tab[7] = DicoLine[_possibleField[7]]

    if _possibleField[2] in DicoLine.keys():
        if DicoLine[_possibleField[2]]:
            tab[2] = DicoLine[_possibleField[2]]

    if _possibleField[3] in DicoLine.keys():
        if DicoLine[_possibleField[3]]:
            tab[3] = DicoLine[_possibleField[3]]

    if _possibleField[4] in DicoLine.keys():
        if DicoLine[_possibleField[4]]:
            tab[4] = DicoLine[_possibleField[4]]

    if _possibleField[5] in DicoLine.keys():
        if DicoLine[_possibleField[5]]:
            tab[5] = DicoLine[_possibleField[5]]

    if _possibleField[8] in DicoLine.keys():
        if DicoLine[_possibleField[8]]:
            tab[8] = DicoLine[_possibleField[8]]

    if _possibleField[9] in DicoLine.keys():
        if DicoLine[_possibleField[9]]:
            tab[9] = DicoLine[_possibleField[9]]

    _cnxObj = PotentialConnexionFromTab(tab)

    return _cnxObj

main()