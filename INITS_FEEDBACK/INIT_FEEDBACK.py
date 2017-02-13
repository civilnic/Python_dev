import pandas as pd
import re
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

from optparse import OptionParser
from MEXICO.CFG.mexico_cfg import mexicoConfig

from FLOT.flot import flot
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
    parser = OptionParser("usage: %prog --xls <xlsFile> --mexico <mexicoCfgFile> --cp <mexicoconceptionFile> "
                          "--cmt <comment> --fuselage --motorization")
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
    globalComment = options.Comment
    _fuselage = options.fuselage
    _motorization = options.motorization


    logger.info("_xlsFile: "+_xlsFile)
    logger.info("_mexicoCfgFile: "+_mexicoCfgFile)
    logger.info("_conceptionFile: "+_conceptionFile)
    logger.info("_fuselage: "+_fuselage)
    logger.info("_motorisation: "+_motorization)
    logger.info("_globalComment: "+globalComment)

    #
    # mexico cfg parsing
    #   Extract informations about MEXICO base.
    #   Informations used here:
    #       _ MEXICO flow file  => allow to set available model list
    #                           => I/O of each of them

    _mexicoCfgObj = mexicoConfig(_mexicoCfgFile)
    _mexicoCfgObj.conceptionFile = _conceptionFile

    # get MEXICO flow file name
    _mexicoFlowFile = _mexicoCfgObj.getFlowFile()

    logger.info("_mexicoFlowFile: "+_mexicoFlowFile)

    #
    # csv parsing
    #  this function will parse CSV File
    #
    parseXlsFile(_xlsFile, _fuselage, _motorization)

    #
    # apply init
    #
    setInitialization(_mexicoCfgObj,_mexicoFlowFile)


def parseXlsFile(xlsFile,fuselage, motorization):

    global _initializationDictPerModel

    # parse MICD file with pandas
    _xl = pd.ExcelFile(xlsFile)

    # init dataframe
    _df = _xl.parse("Inits")

    # empty cell are not "nan" value but None value
    _df = _df.fillna('')

    for index, row in _df.iterrows():

        _modocc = row['Model/Occ']
        _port = row['Port']

        _initValueCellName = fuselage + "_" + motorization
        _value = row[_initValueCellName]

        if _modocc not in _initializationDictPerModel.keys():
            _initializationDictPerModel[_modocc] = {}

        if _port not in _initializationDictPerModel[_modocc].keys():
            _initializationDictPerModel[_modocc][_port] = _value
        else:
            logger.warning("[INIT_FEEDBACK]: Several value specified for port: " + _port +
                           " previous value: " +  _initializationDictPerModel[_modocc][_port])


def setInitialization(mexicoCfgObj,mexicoFlowFile):

    logger.info("*** APPLY INI ***")
    #
    # get Init MICD from MEXICO configuration file
    #
    _initFile = mexicoCfgObj.getInitFilePathName()

    if _initFile:

        if len(_initializationDictPerModel.keys()) > 0:

            logger.info(" MEXICO Init file to update: " + _initFile)

            # Parse MEXICO flot file
            _flotObj = flot(mexicoFlowFile)

            # Parse init file and create MICD object
            _MICD_Inits = Mexico_Init_File(_initFile)

            # Initializations are stored by mod/occ in _initializationDictPerModel dictionary
            # to read only one time each MICD
            for _modocc in sorted(_initializationDictPerModel.keys()):

                # each initialization is then stored by consumer port
                for _port in _initializationDictPerModel[_modocc].keys():

                    logger.info("\n\t[INIT FEEDBACK] Treatment of port: "+_modocc+"/"+_port)

                    # init value to set
                    _initValue = _initializationDictPerModel[_modocc][_port]

                    # if Init value field is empty => set it to 0
                    if _initValue == '':
                        _initValue = 0

                    logger.info("\t\t[INIT FEEDBACK] Required initialization: " + str(_initValue))

                    #
                    # Test port identifier in Mexico base (i.e modocc/port) (check port consistency)
                    #
                    _portObj = _flotObj.getPort(_modocc+"/"+_port)

                    #
                    # if port didn t exist on flow, log a warning and continue with next port
                    #
                    if _portObj is None:
                        logger.warning("\t\t[INIT FEEDBACK] Consumer port didn t exist in MEXICO flot: "
                                       +_modocc+"/"+_port)
                        continue

                    #
                    # get channelObj linked to port object in flow
                    #
                    _channelObj = _portObj.channel

                    logger.info("\t\t[INIT FEEDBACK] Channel linked to consumer port: " + _channelObj.name)

                    # if channel already set in init file
                    # try to get MICD port Obj (i.e. the line corresponding to channel in Initialization MICD)
                    _MICDPortObj = _MICD_Inits.getPortObj(_channelObj.name)

                    # If _MICDPortObj is not None that means that channel is already initialized in Init file.
                    # we have to test the initialized value and change it if different
                    if _MICDPortObj:
                        logger.info("\t\t[INIT FEEDBACK] --> Channel is already initialized in initfile")

                        # if targetted init is None => Init to remove
                        if _initValue is None:
                            logger.info("\t\t[INIT FEEDBACK] init is None => remove from init file")

                            # add init port to initFile
                            _MICD_Inits.RemovePortfromPortObject(_MICDPortObj, "FUN_OUT")

                            continue

                        #
                        # test set value
                        # if value is not the same that targeted value change it in Init file
                        #
                        try:
                            # if channel
                            if (_MICDPortObj.initdefaultvalue is not None) and (_initValue is not None):
                                if float(_MICDPortObj.initdefaultvalue) == float(_initValue):
                                    logger.info("\t\t[INIT FEEDBACK] Equivalent initialization is already set "
                                                "in init file: "+str(_MICDPortObj.initdefaultvalue))
                                    logger.info("\t\t[INIT FEEDBACK] init required: "+str(_initValue))
                                    logger.info("\t\t[INIT FEEDBACK] => nothing to do for this channel ")
                                    continue
                        except ValueError:
                            pass

                        if _MICDPortObj.initdefaultvalue != _initValue:

                            logger.info("\t\t[INIT FEEDBACK] Channel was previously initialized to: "
                                        + str(_MICDPortObj.initdefaultvalue))
                            logger.info("\t\t[INIT FEEDBACK] => is modified to: " + str(_initValue))

                            # change init value
                            _MICDPortObj.initdefaultvalue = checkInitValueConsistency(_initValue,
                                                                                      _MICDPortObj.codingtype)

                            # add modification comment in init file (in description field)
                            _MICDPortObj.description = globalComment

                            # add init port to initFile
                            _MICD_Inits.AddPortfromPortObject(_MICDPortObj, "FUN_OUT")

                            continue

                        else:
                            logger.info("\t\t[INIT FEEDBACK] Channel is already initialized in flot to: "
                                        + _MICDPortObj.initdefaultvalue)
                            logger.info("\t\t[INIT FEEDBACK] => nothing to do for this channel ")

                            continue

                    # channel is not defined in init file
                    else:
                        logger.info("\t\t[INIT FEEDBACK]  --> Channel is not already initialized in initfile")

                        if _channelObj.init is not None:

                            logger.info("\t\t[INIT FEEDBACK] In mexico flow Channel is initialized to: "
                                        + _channelObj.init)

                            try:
                                if (_channelObj.init is not None) and (_initValue is not None):
                                    if float(_channelObj.init) == float(_initValue):
                                        logger.info("\t\t[INIT FEEDBACK] Equivalent initialization is already set "
                                                    "in flot (probably default init from MICD): "
                                                    + str(_channelObj.init))
                                        logger.info("\t\t[INIT FEEDBACK] init required: " + str(_initValue))
                                        logger.info("\t\t[INIT FEEDBACK] => nothing to do for this channel ")
                                        continue

                                if _channelObj.init is not None:
                                    # if channel init is set to 0 => do not add into InitFile
                                    if float(_initValue) == 0.0:
                                        logger.info("\t\tSpecified init not added (null initialization): "
                                                    + str(_initValue))
                                        continue

                            except ValueError:

                                if _channelObj.init == _initValue:
                                    logger.info("\t\t[INIT FEEDBACK] Equivalent initialization is already set "
                                                "in flot (from MICD): " + str(_channelObj.init))
                                    logger.info("\t\t[INIT FEEDBACK] init required in csv: " + str(_initValue))
                                    logger.info("\t\t[INIT FEEDBACK] => nothing to do for this channel ")
                                    continue
                        else:
                            logger.info("\t\t[INIT FEEDBACK] Channel is not yet initialized")

                        # get actor corresponding to modocc in Mexico configuration
                        _actorObj = _mexicoCfgObj.getActor(_modocc)

                        # list micd corresponding to current actor in Mexico configuration
                        # for each micd
                        for _micd in _actorObj.getMICDList():

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

                                _initPort.initdefaultvalue = checkInitValueConsistency(_initValue,
                                                                                       _consPortObj.codingtype)

                                # add init port to initFile
                                _MICD_Inits.AddPortfromPortObject(_initPort, "FUN_OUT")

                                logger.info("\t\t[INIT FEEDBACK] => New channel is added to init file, value set to: "
                                            + str(_initValue))

                                break

            _MICD_Inits.savefile()
        else:
            logger.info("[INIT FEEDBACK] No init to update")
    else:
        #
        # log an error
        #
        pass

def checkInitValueConsistency(initValue,PortType):

    _testOnPortType = re.match(r'(boolean|bool|logical)', str(PortType), re.IGNORECASE)
    _testOnInitValue = re.match(r'(True|False)', str(initValue), re.IGNORECASE)

    # if port type is boolean or logical
    if _testOnPortType:

        # if init value is not True or False
        if not _testOnInitValue:

            if float(initValue) == 0.0:
                _initValue = 'False'
            else:
                _initValue = 'True'
        else:
            _initValue = initValue

    # port type is not logical or boolean
    else:

        # if value is set to True or False
        if _testOnInitValue:

            if initValue.lower() == "false":
                _initValue = 0
            else:
                _initValue = 1

        else:
            _initValue = initValue

    return str(_initValue)

main()