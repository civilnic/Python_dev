"""
Tool to generate ATA31 files for OCASIME MSP
from EIS and SDAC/FWC BDS files this tool could generate:
For each system in EIS/FWC/SDAC:
_ dedicated FDEF MICD
_ associated FDEF .xml file
_ an readable BDS files (.xls format)
_ MEXICO flow for cnx FDEF -> system
"""
import logging
import csv

from os.path import abspath
from logging.handlers import RotatingFileHandler
from datetime import datetime
from optparse import OptionParser
from lxml import etree

from BDS.BDSXLS import BDSXLS
from BDS.BDS_EIS import BDS_EIS
from BDS.BDS_FWC import BDS_FWC
from BDS.BDS_SDAC import BDS_SDAC
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
ToolConfigDict = {}

for sys in ('FWC', 'EIS', 'SDAC'):
    ToolConfigDict[sys]={}
    ToolConfigDict[sys]["Standard_version"] = None
    ToolConfigDict[sys]["BDS"] = None
    ToolConfigDict[sys]["MODEL"] = {}
    ToolConfigDict[sys]["FDEF"] = {}
    ToolConfigDict[sys]["FLOT"] = None

ToolConfigDict['FLOT'] = None


def main():

    global ToolConfigDict
    #
    # Check and take scripts parameters:
    # _ one XML file (tool configuration)
    # _ one or several boolean --eis --fwc --sdac to choose targetted system(s)
    # _ one boolean to activate global flow compuatation betwwen system   --flow
    #
    #

    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.DEBUG)

    # création d'un formateur qui va ajouter le temps, le niveau
    # de chaque message quand on écrira un message dans le log
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    # création d'un handler qui va rediriger une écriture du log vers
    # un fichier en mode 'append', avec 1 backup et une taille max de 1Mo
    file_handler = RotatingFileHandler('MSP_ATA31_GENTOOL.log', 'w', 1000000, 1)

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
    parser = OptionParser("usage: %prog --xml <xmlConfigFile> --fwc --eis --sdac --flot")
    parser.add_option("--xml", dest="xml", help="xml configuration file of the tool",
                      type="string", metavar="FILE")
    parser.add_option("--fwc", dest="fwc", action="store_true", help="activate generation for FWC system")
    parser.add_option("--eis", dest="eis", action="store_true", help="activate generation for EIS system")
    parser.add_option("--sdac", dest="sdac", action="store_true", help="activate generation for SDAC system")
    parser.add_option("--flot", dest="flot", action="store_true", help="activate complete flot (between ATA31 models)"
                                                                       " generation")

    (options, args) = parser.parse_args()

    if len(args) != 0:
        logger.info("incorrect number of arguments")
        parser.error("incorrect number of arguments")

    _xml = options.xml
    _fwc = options.fwc
    _eis = options.eis
    _sdac = options.sdac
    _flot = options.flot

    parseConfigFile(_xml, _fwc, _eis, _sdac, _flot)

    #
    # Treatment for each system:
    # _ parse BDS file
    # _ create both .xml files
    # _ create MICD for FDEF
    # _ create flow between FDEF and dedicated system
    #

    with open(ToolConfigDict["FLOT"], 'w') as csvfile:
        fieldnames = ['Producer_Model / Occ', 'Producer_variable' , 'Operator', 'SDB_Channel_Name', 'Init_Value',
                      'Operator', 'Consumer_Model / Occ', 'Consumer_variable']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()

    if _fwc:
        _syst = 'FWC'

        # parse BDS FWC
        _bdsFWC = BDS_FWC(ToolConfigDict[_syst]["BDS"], _xml)

        _LabelListFWC = ComputeFDEF_XML_BDS(_bdsFWC,_syst)

    if _eis:
        _syst = 'EIS'

        # parse BDS FWC
        _bdsEIS = BDS_EIS(ToolConfigDict[_syst]["BDS"], _xml)

        _LabelListEIS = ComputeFDEF_XML_BDS(_bdsEIS,_syst)

    if _sdac:
        _syst = 'SDAC'

        # parse BDS FWC
        _bdsSDAC = BDS_SDAC(ToolConfigDict[_syst]["BDS"], _xml)

        _LabelListSDAC = ComputeFDEF_XML_BDS(_bdsSDAC,_syst)



def CnxFDEFToSyst(csv_writer,FdefLabelList,syst):

    _modOccFdef = ToolConfigDict[syst]["FDEF"]["MNEMO"]

    for _modoccSyst in ToolConfigDict[syst]["MODEL"].keys():
        pass


    for _labelObj in FdefLabelList:
        pass


#
# Parse XML configuration file for BDS information
#

def ComputeFDEF_XML_BDS(bds_file,syst):

    # Extracted BDS file
    _extractBds = BDSXLS(ToolConfigDict[syst]["ExtractedBDS"], True)

    _version = ToolConfigDict[syst]["FDEF"]["VERSION"]

    _micdFdef = FDEF_MICD(ToolConfigDict[syst]["FDEF"]["MICD"],
                             ToolConfigDict[syst]["FDEF"]["MNEMO"],
                             _version
                             )

    _xmlRootPath = ToolConfigDict[syst]["FDEF"]["XML_PATH"]
    _xmlRootName = ToolConfigDict[syst]["FDEF"]["XML_ROOT_NAME"]

    _xml_conso_file = FDEF_XML(_xmlRootPath + "\\A429_conso_" + _xmlRootName + "_" + _version + ".xml",
                               "A429",
                               source=ToolConfigDict[syst]["BDS"],
                               sourceType="BDS",
                               tool="MSP_ATA31_GENTOOL"
                               )

    _xml_prod_file = FDEF_XML(_xmlRootPath + "\\A429_prod_" + _xmlRootName + "_" + _version + ".xml",
                               "A429",
                               source=ToolConfigDict[syst]["BDS"],
                               sourceType="BDS",
                               tool="MSP_ATA31_GENTOOL"
                               )

    _labelObjList = bds_file.get_LabelObjList(nature="IN", system=syst,
                                             source=ToolConfigDict[syst]["FDEF"]["REGEXP_SOURCES"])

    for labelObj in _labelObjList:
        if len(labelObj.ParameterList) > 0:
            _micdFdef.AddLabelToMICD(labelObj)
            _xml_prod_file.AddLabel(labelObj)
            for parameterObj in labelObj.getParameterList():
              #  parameterObj.labelObj.print(True)
                _extractBds.AddLine(parameterObj)

    print("**bds2xml_file save file**")
    _extractBds.savefile()

    print("**xml_file save file**")
    _xml_conso_file.WriteAndClose()
    _xml_prod_file.WriteAndClose()

    print("**micdFile save file**")
    _micdFdef.savefile()

    return _labelObjList

#
# Parse XML configuration file for BDS information
#

def parseConfigFile(xml_file,flag_fwc,flag_eis,flag_sdac,flag_flot):

    global ToolConfigDict
    """
    Method to parse configuration file
    """
    if xml_file:
        try:
            tree = etree.parse(xml_file)
        except:
            print("Cannot open ATA31 tool configuration file: " + xml_file)
            return None

    for _elem in tree.xpath("/MSP_ATA31/flot"):
        ToolConfigDict["FLOT"] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))

    #
    #  FWS
    #

    if flag_fwc:

        # local var ro design system
        _syst = "FWC"

        # root path of systeme information in XML config file
        _xmlRootPath = "/MSP_ATA31/FWC/"

        ExtractXML(tree, _syst, _xmlRootPath)

    if flag_eis:

        # local var ro design system
        _syst = "EIS"

        # root path of systeme information in XML config file
        _xmlRootPath = "/MSP_ATA31/EIS/"

        ExtractXML(tree, _syst, _xmlRootPath)


    if flag_sdac:
        # local var ro design system
        _syst = "SDAC"

        # root path of systeme information in XML config file
        _xmlRootPath = "/MSP_ATA31/SDAC/"

        ExtractXML(tree, _syst, _xmlRootPath)


def ExtractXML(xml_tree, syst, xmlRootPath):

    global ToolConfigDict

    # FWS BDS informations
    for _elem in xml_tree.xpath(xmlRootPath+"BDS"):
        ToolConfigDict[syst]["BDS"] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))

    for _elem in xml_tree.xpath(xmlRootPath+"BDS/ExtractedBDS"):
        ToolConfigDict[syst]["ExtractedBDS"] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))

    # FWS Model informations
    for _elem in xml_tree.xpath(xmlRootPath+"Model"):


        # get  modele/occurence  ex: FWC_1/1
        _modocc = _elem.get("mnemo") + '/' + _elem.get("occ")

        if _modocc not in ToolConfigDict[syst]["MODEL"].keys():
            ToolConfigDict[syst]["MODEL"][_modocc] = {}

        ToolConfigDict[syst]["MODEL"][_modocc]['MICD'] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))

        # FWS regexp informations
        for _elem in xml_tree.xpath(xmlRootPath+"Model/regexp_A429words"):
            if _elem.get("in") == "N/A":
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_IN'] = None
            else:
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_IN'] = _elem.get("in")

            if _elem.get("out") == "N/A":
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_OUT'] = None
            else:
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_OUT'] = _elem.get("out")

        for _elem in xml_tree.xpath(xmlRootPath+"/Model/regexp_A429refresh"):
            if _elem.get("in") == "N/A":
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_REFRESH_IN'] = None
            else:
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_REFRESH_IN'] = _elem.get("in")

            if _elem.get("out") == "N/A":
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_REFRESH_OUT'] = None
            else:
                ToolConfigDict[syst]["MODEL"][_modocc]['CNX_REGEXP_A429_REFRESH_OUT'] = _elem.get("out")
                # FWS Model informations

    # FWS FDEF Model informations
    for _elem in xml_tree.xpath(xmlRootPath+"fdef"):

        # get  modele/occurence
        ToolConfigDict[syst]["FDEF"]["MNEMO"] = _elem.get("mnemo") + '/' + _elem.get("occ")
        # MICD file for Fdef generation
        ToolConfigDict[syst]["FDEF"]["MICD"] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))
        ToolConfigDict[syst]["FDEF"]["VERSION"] = _elem.get("version")


        # FWS FDEF regexp informations
        for _elem in xml_tree.xpath(xmlRootPath+"fdef/regexp_Source"):
            ToolConfigDict[syst]["FDEF"]["REGEXP_SOURCES"] = _elem.get("regexp")

        for _elem in xml_tree.xpath(xmlRootPath+"fdef/regexp_A429words"):
            if _elem.get("in") == "N/A":
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_IN'] = None
            else:
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_IN'] = _elem.get("in")

            if _elem.get("out") == "N/A":
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_OUT'] = None
            else:
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_OUT'] = _elem.get("out")

        for _elem in xml_tree.xpath(xmlRootPath+"fdef/regexp_A429refresh"):
            if _elem.get("in") == "N/A":
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_REFRESH_IN'] = None
            else:
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_REFRESH_IN'] = _elem.get("in")

            if _elem.get("out") == "N/A":
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_REFRESH_OUT'] = None
            else:
                ToolConfigDict[syst]["FDEF"]['CNX_REGEXP_A429_REFRESH_OUT'] = _elem.get("out")

        for _elem in xml_tree.xpath(xmlRootPath+"fdef/xml_files"):
            ToolConfigDict[syst]["FDEF"]["XML_PATH"] = abspath(_elem.get("path"))
            ToolConfigDict[syst]["FDEF"]["XML_ROOT_NAME"] = _elem.get("root_name")

        for _elem in xml_tree.xpath(xmlRootPath+"flot"):
            ToolConfigDict[syst]["FLOT"] = abspath(_elem.get("path") + '\\' + _elem.get("filename"))


main()