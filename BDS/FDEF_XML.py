from lxml import etree
from datetime import datetime
from A429 import (A429Label,A429ParamDIS,A429ParamBNR,A429ParamBCD,A429ParamOpaque)

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
        self.WriteAndClose()

    #
    # create a new structure (empty) of FDEF XML file
    #
    def fileInit(self):

        # date computation for information
        _date=datetime.now()
        _displaydate=str(_date.day)+"/"+str(_date.month)+"/"+str(_date.year)

        # set the document root name 'configurationTable'
        self._RootElement = etree.Element('configurationTable', type=self.Type, generationDate=_displaydate, generationTool="outil perso")

        # add configurationSources and sourceFile XML element into XML tree
        _configSource = etree.SubElement(self._RootElement, "configurationSources")
        etree.SubElement(_configSource, "sourceFile", type="", pathname="")

        # create configurationEntity, it will be the root element of A429Label sub element
        self._LabelRootElement = etree.SubElement(self._RootElement, "configurationEntity")
    #
    # Finalyse and write XML tree into output document
    #
    def WriteAndClose(self):

        _tree = etree.ElementTree(self._RootElement)
        outFile = open(self.PathName, 'wb')
        _tree.write(outFile, pretty_print=True)
        outFile.close()

    def AddLabel(self, labelObj):

        self._LabelCurrentElement = etree.SubElement(
                                                        self._LabelRootElement, "A429Label",
                                                        name=labelObj.SimuFormattedName, type=labelObj.labeltype,
                                                        labelNumber=labelObj.number, sdi=labelObj.sdi
                                                     )

        _ssmElement=etree.SubElement(self._LabelCurrentElement, "ssm", type=labelObj.labeltype)

        etree.SubElement(
            self._LabelCurrentElement, "ssm",
            name=labelObj.SimuFormattedName+"_SSM", type=labelObj.labeltype,
            labelNumber=labelObj.number, sdi=labelObj.sdi
        )