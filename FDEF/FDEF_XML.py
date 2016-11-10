from datetime import datetime

from lxml import etree

from A429.A429 import (A429ParamBNR, A429ParamBCD)


class FDEF_XML:
    """
    Class to manipulate generic FDEF XML FILES
    """


    def __init__(self, pathname, type):
        """
        Attributes are:
        _ path name of the file
        """

        self.PathName = pathname
        self.Type = type

        self.sourceInfos = None
        self._doc = None
        self._RootElement = None
        self._LabelRootElement = None
        self._LabelCurrentElement = None

        @property
        def sourceInfos(self):
            return self.sourceInfos
        @sourceInfos.setter
        def sourceInfos(self, sourceInfos):
            self.sourceInfos = sourceInfos

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
            generationTool="outil perso"
        )

        # add configurationSources and sourceFile XML element into XML tree
        _configSource = etree.SubElement(
                                            self._RootElement,
                                            "configurationSources"
                                         )
        etree.SubElement(
            _configSource,
            "sourceFile",
            type="",
            pathname=""
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

        _ssmElement = etree.SubElement(
                                        self._LabelCurrentElement,
                                        "ssm",
                                        type=self.getSsmType(labelObj)
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

        _parameterElement = etree.SubElement(
            self._LabelCurrentElement,
            "parameter",
            name=ParamObj.name,
            type=ParamObj.codingtype,
            comment=ParamObj.parameter_def
        )

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
            print("[FDEF_XML]{AddPatameter] Unknwon param coding type: " + ParamObj.codingtype)






    def getSsmType(self, labelObj):

        # if ssmtype attribute is set on object (i.e specified on BDS) we use it here
        if labelObj.ssmtype:
            _ssmtype = FDEF_XML.ssmType(labelObj)

        # we test labeltype field of label object
        # in case of HYB label, ssm type depends on parameters types
        if labelObj.labeltype == "HYB":

            # we parse parameters list of current label
            # if one parameter is BNR => status will be BNR type
            # if one parameter is BCD => status will be BCD type
            # else status is set to default value: no SSM
            for paramobj in labelObj.ParameterList:
                if paramobj.formatparam == "BNR":
                    _ssmtype = "status_ssm_bnr"
                    break
                elif paramobj.formatparam == "BCD":
                    _ssmtype = "status_ssm_bcd"
                    break
                else:
                    _ssmtype = "status_no_ssm"
                pass
        # for other label type DW/BCD/BNR ssm type follow label type
        # => directly converted with ssmType function
        else:
            _ssmtype = FDEF_XML.ssmType(labelObj)
        return _ssmtype

    # set ssmtype according to label type.
    def ssmType(labelObj):
        _ssmtype=None
        if labelObj.labeltype == "BNR":
            _ssmtype = "status_ssm_bnr"
        elif labelObj.labeltype == "DW":
            _ssmtype = "status_ssm_dis"
        elif labelObj.labeltype == "BCD":
            _ssmtype = "status_ssm_bcd"
        else:
            _ssmtype = "status_no_ssm"
        return _ssmtype