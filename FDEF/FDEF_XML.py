from datetime import datetime

from lxml import etree

from A429.A429 import (A429ParamBNR, A429ParamBCD, A429ParamISO5, A429ParamOpaque)


class FDEF_XML:
    """
    Class to manipulate generic FDEF XML FILES
    """


    def __init__(self, pathname, type, source=None,sourceType=None, tool=None):
        """
        Attributes are:
        _ path name of the file
        """

        self.PathName = pathname
        self.Type = type

        self._sourceInfos = source
        self._sourceType = sourceType
        self._generationTool = tool
        self._doc = None
        self._RootElement = None
        self._LabelRootElement = None
        self._LabelCurrentElement = None

        self.fileInit()
       # self.WriteAndClose()

    #
    # create a new structure (empty) of FDEF XML file
    #
    def fileInit(self):

        # date computation for information
        _date=datetime.now()
        _displaydate=str(_date.day)+"/"+str(_date.month)+"/"+str(_date.year)

        # set the document root name 'configurationTable'
        self._RootElement = etree.Element(
            'configurationTable',
            type=self.Type,
            generationDate=_displaydate,
            generationTool=self._generationTool
        )

        # add configurationSources and sourceFile XML element into XML tree
        _configSource = etree.SubElement(
                                            self._RootElement,
                                            "configurationSources"
                                         )
        etree.SubElement(
            _configSource,
            "sourceFile",
            type=self._sourceType,
            pathname=self._sourceInfos
        )

        # create configurationEntity, it will be the root element of A429Label sub element
        self._LabelRootElement = etree.SubElement(
            self._RootElement,
            "configurationEntity"
        )
    #
    # Finalyse and write XML tree into output document
    #
    def WriteAndClose(self):

        _tree = etree.ElementTree(self._RootElement)
        outFile = open(self.PathName, 'wb')
        _tree.write(outFile, pretty_print=True)
        outFile.close()

    def AddLabel(self, labelObj):

        # DW label type is identified as DIS label in FDEF XML file
        if labelObj.labeltype == "DW":
            _labelType = "DIS"
        else:
            _labelType = labelObj.labeltype

        self._LabelCurrentElement = etree.SubElement(
                                                        self._LabelRootElement,
                                                        "A429Label",
                                                        name=labelObj.SimuFormattedName,
                                                        type=_labelType,
                                                        labelNumber=str("%.3d" % labelObj.number),
                                                        sdi=labelObj.sdi
                                                     )
        # convert ssm type for FDEF
        if labelObj.ssmtype == "BNR":
            _ssmtype = "status_ssm_bnr"
        elif labelObj.ssmtype == "DW":
            _ssmtype = "status_ssm_dis"
        elif labelObj.ssmtype == "BCD":
            _ssmtype = "status_ssm_bcd"
        elif labelObj.ssmtype == "":
            _ssmtype = "status_no_ssm"

        _ssmElement = etree.SubElement(
                                        self._LabelCurrentElement,
                                        "ssm",
                                        type=_ssmtype
                                     )

        _parameterElement = etree.SubElement(
            _ssmElement,
            "parameter",
            name=labelObj.SimuFormattedName+"_SSM",
            type="status",
            comment="SSM of label " + labelObj.SimuFormattedName
        )

        etree.SubElement(
            _parameterElement, "signal",
            name=labelObj.SimuFormattedName + "_SSM"
        )

        for ParamObj in labelObj.ParameterList:
            self.AddParameter(ParamObj)

    def AddParameter(self, ParamObj):

        if isinstance(ParamObj, A429ParamISO5) or isinstance(ParamObj, A429ParamOpaque):
            _parameterElement = etree.SubElement(
                self._LabelCurrentElement,
                "parameter",
                name=ParamObj.name,
                type="String",
                comment=ParamObj.parameter_def
            )
        else:
            _parameterElement = etree.SubElement(
                self._LabelCurrentElement,
                "parameter",
                name=ParamObj.name,
                type=ParamObj.codingtype,
                comment=ParamObj.parameter_def
            )

        if isinstance(ParamObj, A429ParamISO5):
            _signalElement = etree.SubElement(
                _parameterElement,
                "signal",
                name=ParamObj.SimuPreFormattedName,
                type=ParamObj.codingtype,
                nbBit=str(ParamObj.nb_bits),
                lsb=str(ParamObj.lsb),
                msb=str(ParamObj.msb),
                signed="0",
                startBit="1",
                comment=ParamObj.parameter_def
            )
        else:
            _signalElement = etree.SubElement(
                _parameterElement,
                "signal",
                name=ParamObj.SimuPreFormattedName,
                type=ParamObj.codingtype,
                nbBit=str(ParamObj.nb_bits),
                lsb=str(ParamObj.lsb),
                msb=str(ParamObj.msb),
                signed=str(ParamObj.signed),
                startBit="1",
                comment=ParamObj.parameter_def
            )

        if isinstance(ParamObj, A429ParamBNR):
            _paramType = "BNR"
        elif isinstance(ParamObj, A429ParamBCD):
            _paramType = "BCD"
        else:
            return None
            #TODO : add other param type specification into XML

        if ParamObj.codingtype == "float":
            etree.SubElement(
                _signalElement,
                "float",
                floatResolution=str(ParamObj.resolution),
                floatCodingType=_paramType
            )
        elif ParamObj.codingtype == "int":
            etree.SubElement(
                _signalElement,
                "integer",
                integerResolution=str(ParamObj.resolution),
                integerCodingType=_paramType
            )
        else:
            ParamObj.print()
            print("[FDEF_XML]{AddPatameter] Unknwon param coding type: " + ParamObj.codingtype)
