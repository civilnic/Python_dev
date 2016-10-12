from lxml import etree

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
        self.doc = None

        self._RootElement = None
        self._LastElement = None

        @property
        def File(self):
            return self.File
        @File.setter
        def File(self, File):
            self.File = File

        self.fileInit()

    def fileInit(self):

        rootElement = etree.Element('configurationTable')
        self.doc = etree.ElementTree(rootElement)

        outFile = open(self.PathName, 'w')
        self.doc.write(outFile)
        outFile.close()