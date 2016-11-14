import os
from lxml import etree


class mexicoConfig:

    def __init__(self, pathname):

        try:
            with open(pathname):
                pass
        except IOError:
            print ("[mexicoConfig][init] Cannot open MEXICO config file: "+str(pathname))

        self.fileName = os.path.basename(pathname)
        self.filePath = os.path.dirname(pathname)
        self.pathName = pathname

        self._mexicoRootPath = None
        self._actors = []
        self._initFile = {}
        self._ssdbFiles = {}


        print("fileName: " + self.fileName)
        print("filePath: " + self.filePath)

        self.parse()

    def parse(self):

        tree = etree.parse(self.pathName)

        root = tree.getroot()

        for element in root.iter("*"):

            # mexico configuration
            if element.tag == "Config":

                if element.attrib['dataDirWin']:
                    self._mexicoRootPath = os.path.abspath(self.filePath+"\\"+element.attrib['dataDirWin'])

            # ssdb file are listed in Base elements
            if element.tag == "Base":

                if element.attrib['fileName'] and element.attrib['type']:

                    self.addSSDB(element.attrib['fileName'], element.attrib['type'])

                else:
                    continue

            #  model tag are named Actor
            if element.tag == "Actor":

                _model = element.attrib['name']+"/"+element.attrib['occurrence']

                _actorObj = Actor(_model)
                _actorObj.mexicoRootPath = self._mexicoRootPath

                self.addActor(_actorObj)

                # get MICD element list
                _micdelementList = element.getchildren()

                for _micdelement in _micdelementList:

                    _MICDObj = mexicoMICDFile(_micdelement.attrib['fileName'],_micdelement.attrib['type'],_actorObj)

                    _actorObj.addMICD(_MICDObj)

                    _couplingElementList = _micdelement.getchildren()

                    for _couplingElement in _couplingElementList:

                        _couplingObj = mexicoCouplingFile(_couplingElement.attrib['fileName'],
                                                          _couplingElement.attrib['type'],
                                                          _couplingElement.attrib['editable'],
                                                          _MICDObj)
                        _MICDObj.addCoupling(_couplingObj)
            #rint(element.attrib)


    def addActor(self,actorObj):
        if actorObj not in self._actors:
            self._actors.append(actorObj)



    def isSSDB(self,ssdb):

        _fullPath = os.path.abspath(ssdb)

        if _fullPath in self._ssdbFiles.keys():
            return True
        else:
            return False

    def addSSDB(self,ssdb,type):

        _filename = os.path.basename(ssdb)
        _relativPath = os.path.dirname(ssdb)
        _fullPath = os.path.abspath(self._mexicoRootPath + "\\" + _relativPath + "\\" + _filename)

        if not self.isSSDB(_fullPath):
            self._ssdbFiles[_fullPath] = {
                'filename': _filename,
                'relativPath': _relativPath,
                'type': type
            }
            return True
        else:
            return False





class Actor:

    def __init__(self, actorname):
        self._name = actorname
        self._micds = []
        self._couplingFiles = {}
        self._mexicoRootPath = "."

    @property
    def name(self):
        return self._name

    @property
    def mexicoRootPath(self):
        return self._mexicoRootPath
    @mexicoRootPath.setter
    def mexicoRootPath(self, mexicoRootPath):
        self._mexicoRootPath = mexicoRootPath

    def addMICD(self, micdObj):
        if micdObj not in self._micds:
            self._micds.append(micdObj)


class mexicoMICDFile:

    def __init__(self, micdname,type,actor):

        self._filename = os.path.basename(micdname)
        self._relativPath = os.path.dirname(micdname)
        self. _fullPathName = os.path.abspath(actor.mexicoRootPath + "\\" + self._relativPath + "\\" + self._filename)
        self._type = type
        self._actor = actor
        self._couplingFiles = []

    @property
    def fullPathName(self):
        return self._fullPathName

    @property
    def type(self):
        return self._type

    @property
    def mexicoRootPath(self):
        return self._actor.mexicoRootPath

    def addCoupling(self,couplingObj):
        if couplingObj not in self._couplingFiles:
            self._couplingFiles.append(couplingObj)


class mexicoCouplingFile:

    def __init__(self, couplingname,type,writable,micd):
        self._filename = os.path.basename(couplingname)
        self._relativPath = os.path.dirname(couplingname)
        self._micd = micd
        self. _fullPathName = os.path.abspath(micd.mexicoRootPath + "\\" + self._relativPath + "\\" + self._filename)
        self._type = type
        self._writable = writable

    @property
    def fullPathName(self):
        return self._fullPathName

    @property
    def type(self):
        return self._type

    @property
    def writable(self):
        return self._writable