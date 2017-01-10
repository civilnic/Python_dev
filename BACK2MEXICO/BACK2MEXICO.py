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
from MEXICO.INIT.mexico_inits import Mexico_Init_File

# date computation for information
_date = datetime.now()
displayDate = str(_date.day) + "/" + str(_date.month) + "/" + str(_date.year)

# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger()

comment = None

#
# dictionary of alias modification to do per model
#
_aliasConsDict = {}
_aliasProdDict = {}
_initializationDict = {}

_mexicoCfgObj = None


def main():

    global _mexicoCfgObj, comment, logger

    # date computation for information
    _date = datetime.now()

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

    logger.info("************************************************")
    logger.info(" BACK2MEXICO tool")
    logger.info("************************************************")
    logger.info(" RUN informations:")
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
    s = " - ";
    logger.info("\tList of common models between flow files\n" + s.join(sorted(_commonModels)))

    #
    # loop on common models
    #

    for _model in sorted(_commonModels):

        logger.info("\tTreatment of model: " + _model)

        #
        # on both flow get the corresponding model object
        #
        _mexicoModelObj = _mexicoFlotObj.getModel(_model)
        _cnxmModelObj = _cnxmFlotObj.getModel(_model)

        #
        # for each model create a list of consumers ports
        #
        _mexicoConsList = []
        _cnxmConsList = []
        _mexicoConsDict = dict()
        _cnxmConsDict = dict()

        for _portObj in _mexicoModelObj.ports_consum:
            _mexicoConsList.append(_portObj.name)
            _mexicoConsDict[_portObj.name] = _portObj
        for _portObj in _cnxmModelObj.ports_consum:
            _cnxmConsList.append(_portObj.name)
            _cnxmConsDict[_portObj.name] = _portObj
        #
        # create a list of common ports (only common ports could be treated by this script)
        #
        _commonConsumers = [x for x in _cnxmConsList if x in _mexicoConsList]

        #
        # loop on common port name
        #

        for _port in sorted(_commonConsumers):

            #
            # port is uniquely identified in flow with the identifier: mod/occ/port
            # recreate local port identifier here
            #

            _portIdent = _model+"/"+_port

            #
            # create a connexion object from both flow
            #

            _mexicoCNXObj = _mexicoFlotObj.getCnxForPort(_portIdent)
            _cnxmCNXObj = _cnxmFlotObj.getCnxForPort(_portIdent)

            #
            # evaluate connexion object from cnxm in mexico flow
            # return a comparison result tab
            #
            _compResTab = _mexicoFlotObj.compCnx(_cnxmCNXObj)

            # there is difference to report on mexico flow
            # differences analysis and translation in term of aliases on modele/port
            if _compResTab != [False] * 10:
                print(_compResTab)
                print(_mexicoCNXObj)
                print(_cnxmCNXObj)

                #
                # create an alias object for producer and consumer to be
                # used if modification are needed
                #
                _consCnxmAlias = _cnxmCNXObj.getConsAlias()
                _prodCnxmAlias = _cnxmCNXObj.getProdAlias()

                _TargetConsCnxmAliasObj = MexicoAlias(AliasObj=_consCnxmAlias, date=displayDate, comment=comment)
                _TargetProdCnxmAliasObj = MexicoAlias(AliasObj=_prodCnxmAlias, date=displayDate, comment=comment)

                #
                # comparison algorithm
                #
                # there is a signal difference => coupling on producer and consumer must be modified
                #
                if _compResTab[4]:

                    # add new alias on consumer
                    AddAlias(_TargetConsCnxmAliasObj, _mexicoConsDict[_port])

                    # if producer is defined on cnxm flow and producer exist on mexico flow
                    # add a new alias on producer also
                    if _cnxmCNXObj.portProd:

                        #
                        # check that producer specified in cnxm flow exist on mexico flow:
                        #
                        if _cnxmCNXObj.getProdTriplet():

                            #
                            # get port object on mexico flow for producer
                            #
                            _prodPortObj = _mexicoFlotObj.getPort(_cnxmCNXObj.getProdTriplet())

                            #
                            # add new alias on producer
                            #
                            AddAlias(_TargetProdCnxmAliasObj, _prodPortObj)

                        else:
                            logger.warning("[BACK2MEXICO] -- Producer port didn t exist on mexico flow: "
                                           + _cnxmCNXObj.modoccProd  + "/" + _cnxmCNXObj.portProd + "--\n\t\t ")
                            pass

                else:
                    #
                    # new operator or tab on producer to set
                    #
                    if _compResTab[2] or _compResTab[3]:

                        #
                        # check that producer specified in cnxm flow exist on mexico flow:
                        #
                        if _cnxmCNXObj.getProdTriplet():

                            #
                            # get port object on mexico flow for producer
                            #
                            _prodPortObj = _mexicoFlotObj.getPort(_cnxmCNXObj.getProdTriplet())

                            #
                            # add new alias on producer
                            #
                            AddAlias(_TargetProdCnxmAliasObj, _prodPortObj)

                        else:
                            logger.warning("[BACK2MEXICO] -- Producer port didn t exist on mexico flow: "
                                           + _cnxmCNXObj.modoccProd  + "/" + _cnxmCNXObj.portProd + "--\n\t\t ")
                            pass
                    #
                    # difference on consumer operator or tab
                    #
                    if _compResTab[8] or _compResTab[9]:
                        #
                        # add new alias on consumer
                        #
                        AddAlias(_TargetConsCnxmAliasObj, _mexicoConsDict[_port])

                #
                # there is an init difference
                #
                if _compResTab[5]:

                    # create a channel object (ChannelObj)
                    from FLOT.channel import channel
                    channelObj = channel(_cnxmCNXObj.Channel)

                    # add the initialization value
                    channelObj.init = _cnxmCNXObj.init

                    # link it consumer port
                    channelObj.addPort(_mexicoConsDict[_port])

                    # add to inits dictionary
                    AddInit(channelObj, _mexicoConsDict[_port])

            # no difference for cnx  => nothing to doq
            else:
                pass

    print("**** ALIAS PROD ****")
    for modele in _aliasProdDict.keys():

        actorObj = _mexicoCfgObj.getActor(modele)

        _coulingFileObj = mexico_coupling(actorObj.getFirstCplFile())

        print('modele: ' + modele)

        if _aliasProdDict[modele]:

            for port in sorted(_aliasProdDict[modele].keys()):
                print('port: ' + port)
                print(_aliasProdDict[modele][port])

                _coulingFileObj.chgAddModify(_aliasProdDict[modele][port], "FUN_OUT")

        _coulingFileObj.write()

    print("**** ALIAS CONSO ****")
    for modele in _aliasConsDict.keys():

        actorObj = _mexicoCfgObj.getActor(modele)

        _coulingFileObj = mexico_coupling(actorObj.getFirstCplFile())

        print('modele: ' + modele)

        if _aliasConsDict[modele]:

            for port in sorted(_aliasConsDict[modele].keys()):
                print('port: ' + port)
                print(_aliasConsDict[modele][port])

                _coulingFileObj.chgAddModify(_aliasConsDict[modele][port], "FUN_IN")

        _coulingFileObj.write()

    print("**** INIT ****")
    #
    # get Init MICD from MEXICO configuration file
    #
    _initFile=_mexicoCfgObj.getInitFilePathName()
    logger.info(" MEXICO Init file updated: " + _initFile)

    if _initFile:

        _MICD_Inits=Mexico_Init_File(_initFile)

        for _portObj in _MICD_Inits.getPortObjList():
            print(_portObj.getPortLineTab())

        for channel in sorted(_initializationDict.keys()):
            print('channel: ' + channel)
            print('value: ' + str(_initializationDict[channel].init))

    else:
        #
        # log an error
        #
        pass

# fill dictionary of coupling to be done from alias object
# to sort coupling by model

def AddAlias(aliasObj, portObj):

    global logger, _aliasConsDict, _aliasProdDict

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
            logger.warning("[BACK2MEXICO][AddAlias] -- Several connections specified for port: "
                           + portObj.getIdentifier() + "--\n\t\t ")


#
# fill dictionary of init to be done
# sort init by model

def AddInit(channelObj, portObj):

    # target dictionary
    _dict = _initializationDict

    # test if model assoicate to port is alreday in init dict
    # else create an empty dict for model key
    if channelObj.name not in _dict.keys():
        _dict[channelObj.name] = channelObj
    else:

        if channelObj.init != _dict[channelObj.name].init:

            logger.warning("[BACK2MEXICO][AddInit] -- Several initializations specified for port: "
                           + portObj.getIdentifier + "--\n\t\tCannot set init: " + str(channelObj.init) + " because it"
                                                                                                          " as "
                                                                    " already set to: " + _dict[channelObj.name].init)

main()