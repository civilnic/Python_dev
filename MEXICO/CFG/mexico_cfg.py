import os
from lxml import etree


class mexicoConfig:

    def __init__(self, pathname):

        try:
            with open(pathname):
                pass
        except IOError:
            print("[mexicoConfig][init] Cannot open MEXICO config file: "+str(pathname))

        self.fileName = os.path.basename(pathname)
        self.filePath = os.path.dirname(pathname)
        self.pathName = pathname
        self._conceptionFile = None

        self._mexicoRootPath = None     # set during parsing
        self._flowFilePathName = None           # set during parsing
        self._flowFileName = "ALL-SIMU_FLOW.csv"
        self._flowFilePath = None       # set during parsing

        self._actors = []
        self._initFile = []
        self._ssdbFiles = []

        self.parse()

    @property
    def conceptionFile(self):
        return self._conceptionFile

    @conceptionFile.setter
    def conceptionFile(self, conceptionFile):
        self._conceptionFile = conceptionFile
        _flowRelativPath = self.conception()

        self._flowFilePath = os.path.abspath(self._mexicoRootPath + '\\' + _flowRelativPath)
        self._flowFilePathName = self._flowFilePath + "\\" + self._flowFileName

    # function to get flow relativ path
    def conception(self):
        try:
            with open(self.conceptionFile):
                pass
        except IOError:
            print("[mexicoConfig][conception] Cannot open MEXICO conception file: "+str(self.conceptionFile))
            exit(1)

        tree = etree.parse(self.conceptionFile)

        root = tree.getroot()

        for element in root.iter("*"):

            #  model tag are named Actor
            if element.tag == "Template":

                # cnx flow
                if element.attrib['name'] == "cnxflow":

                    # get MICD element list
                    for subElement in element.iter("*"):

                        #  model tag are named Actor
                        if subElement.tag == "Outputs":

                            return subElement.attrib['dirWin']



    def parse(self):

        try:
            tree = etree.parse(self.pathName)
        except OSError:
            print("[mexicoConfig][ssdb configuration]: Cannot open MEXICO SSDB configuration file"+self.pathName)
            exit(1)

        root = tree.getroot()

        for element in root.iter("*"):

            # mexico configuration
            if element.tag == "Config":

                if element.attrib['dataDirWin']:
                    self._mexicoRootPath = os.path.abspath(self.filePath+"\\"+element.attrib['dataDirWin'])

            # ssdb file are listed in Base elements
            if element.tag == "Base":

                _ssdbfileObj = mexicoSSDBFile(element.attrib['fileName'], element.attrib['type'], self._mexicoRootPath)
                self.addSSDB(_ssdbfileObj)

            #  model tag are named Actor
            if element.tag == "Actor":

                _model = element.attrib['name']+"/"+element.attrib['occurrence']

                _actorObj = Actor(_model)
                _actorObj.mexicoRootPath = self._mexicoRootPath

                self.addActor(_actorObj)

                # get MICD element list
                _micdelementList = element.getchildren()

                for _micdelement in _micdelementList:

                    _MICDObj = mexicoMICDFile(_micdelement.attrib['fileName'], _micdelement.attrib['type'] ,_actorObj)
                    _actorObj.addMICD(_MICDObj)

                    _couplingElementList = _micdelement.getchildren()

                    for _couplingElement in _couplingElementList:

                        _couplingObj = mexicoCouplingFile(_couplingElement.attrib['fileName'],
                                                          _couplingElement.attrib['type'],
                                                          _couplingElement.attrib['editable'],
                                                          _MICDObj)
                        _MICDObj.addCoupling(_couplingObj)
                        _actorObj.addCoupling(_couplingObj)

            #  init file tag is named ActorInit
            if element.tag == "ActorInit":

                # get MICD element list
                _micdelementList = element.getchildren()

                _actorObj = Actor(_model)
                _actorObj.mexicoRootPath = self._mexicoRootPath

                self.addActorInit(_actorObj)

                for _micdelement in _micdelementList:

                    _InitMICDObj = mexicoMICDFile(_micdelement.attrib['fileName'], _micdelement.attrib['type'] , _actorObj)
                    _actorObj.addMICD(_InitMICDObj)



            #rint(element.attrib)

    def addSSDB(self,ssdbObj):
        if ssdbObj not in self._ssdbFiles:
            self._ssdbFiles.append(ssdbObj)

    def addActorInit(self,actorObj):
        if actorObj not in self._initFile:
            self._initFile.append(actorObj)

    def addActor(self,actorObj):
        if actorObj not in self._actors:
            self._actors.append(actorObj)

    def getActor(self,actorName):
        for _actorObj in self.getActorList():
            if _actorObj.name == actorName:
                return _actorObj
            else:
                _actorObj = None
                pass

    def getActorList(self):
        return self._actors

    def getNbActor(self):
        return len(self._actors)

    def getMexicoRootPath(self):
        return self._mexicoRootPath

    def getInitFilePathName(self):

        if self._initFile:
            _InitActorObj = self._initFile[0]
            _InitActorMicd = _InitActorObj.getMICDList()[0]
            return _InitActorMicd.fullPathName
        else:
            return None

    def getFlowFile(self):

        if self._flowFilePathName:
            return self._flowFilePathName
        else:
            return None

class Actor:

    def __init__(self, actorname):
        self._name = actorname
        self._micds = []
        self._couplingFiles = []
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

    def getMICDList(self):
        return self._micds

    def addCoupling(self,couplingObj):
        if couplingObj not in self._couplingFiles:
            self._couplingFiles.append(couplingObj)

    def getCplList(self):
        return self._couplingFiles

    def getFirstCplFile(self):
        if self._couplingFiles[0]:
            return self._couplingFiles[0].fullPathName
        else:
            None


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

    def getCouplingObjList(self):
        return self._couplingFiles

class mexicoCouplingFile:

    def __init__(self, couplingname, type, writable, micd):
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



class mexicoSSDBFile:

    def __init__(self, ssdbname,type, mexicoRootPath):

        self._filename = os.path.basename(ssdbname)
        self._relativPath = os.path.dirname(ssdbname)
        self. _fullPathName = os.path.abspath(mexicoRootPath + "\\" + self._relativPath + "\\" + self._filename)

    @property
    def fullPathName(self):
        return self._fullPathName

    @property
    def type(self):
        return self._type