
class MICD_port:
    """
    Class to desribe port in MICD
    """


    def __init__(self, portTab=None, type=None, configTab=None):

        _refTab = configTab
        print(_refTab)
        print(portTab)
        self.name = None
        self.codingtype = None
        self.unit = None
        self.description = None
        self.convention = None
        self.dim1 = None
        self.dim2 = None
        self.comformat = None
        self.commode = None
        self.fromto = None
        self.resfreshrate = None
        self.min = None
        self.max = None
        self.enum = None
        self.prodconsif = None
        self.aircraftsignalname = None
        self.interfacelevel = None
        self.status = None
        self.simulationlevel  = None
        self.initdefaultvalue = None
        self.notsimudatacustom = None
        self.comment = None
        self.lastmodification = None
        
        self._type = type
        if (portTab is not None) and (_refTab is not None):
            if 'name' in _refTab:
                if portTab[_refTab.index('name')]:
                    self._name = portTab[_refTab.index('name')]
            if 'codingtype' in _refTab:
                if portTab[_refTab.index('codingtype')]:
                    self._codingtype = portTab[_refTab.index('codingtype')]
            if 'unit' in _refTab:
                if portTab[_refTab.index('unit')]:
                    self._unit = portTab[_refTab.index('unit')]
            if 'description' in _refTab:
                if portTab[_refTab.index('description')]:
                    self._description = portTab[_refTab.index('description')]
            if 'convention' in _refTab:
                if portTab[_refTab.index('convention')]:
                    self._convention = portTab[_refTab.index('convention')]
            if 'dim1' in _refTab:
                if portTab[_refTab.index('dim1')]:
                    self._dim1 = portTab[_refTab.index('dim1')]
            if 'dim2' in _refTab:
                if portTab[_refTab.index('dim2')]:
                    self._dim2 = portTab[_refTab.index('dim2')]
            if 'comformat' in _refTab:
                if portTab[_refTab.index('comformat')]:
                    self._comformat = portTab[_refTab.index('comformat')]
            if 'commode' in _refTab:
                if portTab[_refTab.index('commode')]:
                    self._comformat = portTab[_refTab.index('commode')]
            if 'fromto' in _refTab:
                if portTab[_refTab.index('fromto')]:
                    self._fromto = portTab[_refTab.index('fromto')]
            if 'resfreshrate' in _refTab:
                if portTab[_refTab.index('resfreshrate')]:
                    self._resfreshrate = portTab[_refTab.index('resfreshrate')]
            if 'min' in _refTab:
                if portTab[_refTab.index('min')]:
                    self._min = portTab[_refTab.index('min')]
            if 'max' in _refTab:
                if portTab[_refTab.index('max')]:
                    self._max = portTab[_refTab.index('max')]
            if 'enum' in _refTab:
                if portTab[_refTab.index('enum')]:
                    self._enum = portTab[_refTab.index('enum')]
            if 'prodconsif' in _refTab:
                if portTab[_refTab.index('prodconsif')]:
                    self._prodconsif = portTab[_refTab.index('prodconsif')]
            if 'aircraftsignalname' in _refTab:
                if portTab[_refTab.index('aircraftsignalname')]:
                    self._aircraftsignalname = portTab[_refTab.index('aircraftsignalname')]
            if 'interfacelevel' in _refTab:
                if portTab[_refTab.index('interfacelevel')]:
                    self._interfacelevel = portTab[_refTab.index('interfacelevel')]
            if 'status' in _refTab:
                if portTab[_refTab.index('status')]:
                    self._status = portTab[_refTab.index('status')]
            if 'simulationlevel' in _refTab:
                if portTab[_refTab.index('simulationlevel')]:
                    self._simulationlevel = portTab[_refTab.index('simulationlevel')]
            if 'initdefaultvalue' in _refTab:
                if portTab[_refTab.index('initdefaultvalue')]:
                    self._initdefaultvalue = portTab[_refTab.index('initdefaultvalue')]
            if 'notsimudatacustom' in _refTab:
                if portTab[_refTab.index('notsimudatacustom')]:
                    self._notsimudatacustom = portTab[_refTab.index('notsimudatacustom')]
            if 'comment' in _refTab:
                if portTab[_refTab.index('comment')]:
                    self._comment = portTab[_refTab.index('comment')]
            if 'lastmodification' in _refTab:
                if portTab[_refTab.index('lastmodification')]:
                    self._lastmodification = portTab[_refTab.index('lastmodification')]


    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


    @property
    def codingtype(self):
        return self._codingtype

    @codingtype.setter
    def codingtype(self, codingtype):
        self._codingtype = codingtype


    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        self._unit = unit


    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


    @property
    def convention(self):
        return self._convention

    @convention.setter
    def convention(self, convention):
        self._convention = convention


    @property
    def dim1(self):
        return self._dim1

    @dim1.setter
    def dim1(self, dim1):
        self._dim1 = dim1



    @property
    def dim2(self):
        return self._dim2

    @dim2.setter
    def dim2(self, dim2):
        self._dim2 = dim2

    @property
    def comformat(self):
        return self._comformat

    @comformat.setter
    def comformat(self, comformat):
        self._comformat = comformat

    @property
    def commode(self):
        return self._commode

    @commode.setter
    def commode(self, commode):
        self._commode = commode


    @property
    def fromto(self):
        return self._fromto

    @fromto.setter
    def fromto(self, fromto):
        self._fromto = fromto


    @property
    def resfreshrate(self):
        return self._resfreshrate

    @resfreshrate.setter
    def resfreshrate(self, resfreshrate):
        self._resfreshrate = resfreshrate

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, min):
        self._min = min


    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, max):
        self._max = max

    @property
    def enum(self):
        return self._enum

    @enum.setter
    def enum(self, enum):
        self._enum = enum


    @property
    def prodconsif(self):
        return self._prodconsif

    @prodconsif.setter
    def prodconsif(self, prodconsif):
        self._prodconsif = prodconsif


    @property
    def aircraftsignalname(self):
        return self._aircraftsignalname

    @aircraftsignalname.setter
    def aircraftsignalname(self, aircraftsignalname):
        self._aircraftsignalname = aircraftsignalname


    @property
    def interfacelevel(self):
        return self._interfacelevel

    @interfacelevel.setter
    def interfacelevel(self, interfacelevel):
        self._interfacelevel = interfacelevel


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status


    @property
    def simulationlevel(self):
        return self._simulationlevel

    @simulationlevel.setter
    def simulationlevel(self, simulationlevel):
        self._simulationlevel = simulationlevel



    @property
    def initdefaultvalue(self):
        return self._initdefaultvalue

    @initdefaultvalue.setter
    def initdefaultvalue(self, initdefaultvalue):
        self._initdefaultvalue = initdefaultvalue

    @property
    def notsimudatacustom(self):
        return self._notsimudatacustom

    @notsimudatacustom.setter
    def notsimudatacustom(self, notsimudatacustom):
        self._notsimudatacustom = notsimudatacustom

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @property
    def lastmodification(self):
        return self._lastmodification

    @lastmodification.setter
    def lastmodification(self, lastmodification):
        self._lastmodification = lastmodification

    def getPortLineTab(self):

        # tab initialisation
        _portLine = []

        # tab construction
        _portLine.append(self.name)
        _portLine.append(self.codingtype)
        _portLine.append(self.unit)
        _portLine.append(self.description)
        _portLine.append(self.convention)
        _portLine.append(self.dim1)
        _portLine.append(self.dim2)
        _portLine.append(self.comformat)
        _portLine.append(self.fromto)
        _portLine.append(self.resfreshrate)
        _portLine.append(self.min)
        _portLine.append(self.max)
        _portLine.append(self.enum)
        _portLine.append(self.prodconsif)
        _portLine.append(self.aircraftsignalname)
        _portLine.append(self.interfacelevel)
        _portLine.append(self.status)
        _portLine.append(self.simulationlevel )
        _portLine.append(self.initdefaultvalue)
        _portLine.append(self.notsimudatacustom)
        _portLine.append(self.comment)
        _portLine.append(self.lastmodification)

        return _portLine