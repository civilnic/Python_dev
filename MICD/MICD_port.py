
class MICD_port:
    """
    Class to desribe port in MICD
    """
#
#     Port_in_field_equi={
# 'Name': 'name' ,
# 'Type': 'type' ,
# 'Unit': 'unit' ,
# 'Description': 'description',
# 'Convention': 'convention',
# 'Dim1': 'dim1',
# 'Dim2': 'dim2',
# 'Com Format': 'comformat',
# 'Com Mode': 'commode',
# 'From': 'from',
# 'Refresh Rate': 'resfreshrate',
# 'Min': 'min',
# 'Max': 'max',
# 'Enum': 'enum',
# 'Consumed if': 'consumedif',
# 'Aircraft Signal Name': 'aircraftsignalname',
# 'Interface Level': 'interfacelevel',
# 'Status(SSM / FS / Refresh)': 'status',
# 'Simulation Level[1]': 'simulationlevel',
# 'Init Value': 'initvalue',
# 'Custom': 'custom',
# 'Comment': 'comment',
# 'Last modification': 'lastmodification'
#     }

    Port_in_field = [
        'name',
        'type',
        'unit',
        'description',
        'convention',
        'dim1',
        'dim2',
        'comformat',
        'commode',
        'fromto',
        'resfreshrate',
        'min',
        'max',
        'enum',
        'consumedif',
        'aircraftsignalname',
        'interfacelevel',
        'status',
        'simulationlevel',
        'initvalue',
        'custom',
        'comment',
        'lastmodification'
    ]

    Port_out_field = [
        'name',
        'type',
        'unit',
        'description',
        'convention',
        'dim1',
        'dim2',
        'comformat',
        'commode',
        'fromto',
        'resfreshrate',
        'min',
        'max',
        'enum',
        'producedif',
        'aircraftsignalname',
        'interfacelevel',
        'status',
        'simulationlevel',
        'comment',
        'notsimulateddata',
        'defaultvalue',
        'lastmodification'
    ]



    def __init__(self, portTab,type):

        self._type = type

        if self._type == "IN":
            _refTab = MICD_port.Port_in_field
        else:
            _refTab = MICD_port.Port_out_field
            

        self._name = portTab[_refTab.index('name')]
        self._codingtype = portTab[_refTab.index('type')]
        self._unit = portTab[_refTab.index('unit')]
        self._description = portTab[_refTab.index('description')]
        self._convention = portTab[_refTab.index('convention')]
        self._dim1 = portTab[_refTab.index('dim1')]
        self._dim2 = portTab[_refTab.index('dim2')]
        self._comformat = portTab[_refTab.index('comformat')]
        self._fromto = portTab[_refTab.index('fromto')]
        self._resfreshrate = portTab[_refTab.index('resfreshrate')]
        self._min = portTab[_refTab.index('min')]
        self._max = portTab[_refTab.index('max')]
        self._enum = portTab[_refTab.index('enum')]
        self._prodconsif = portTab[_refTab.index('consumedif')]
        self._aircraftsignalname = portTab[_refTab.index('aircraftsignalname')]
        self._interfacelevel = portTab[_refTab.index('interfacelevel')]
        self._status = portTab[_refTab.index('status')]
        self._simulationlevel = portTab[_refTab.index('simulationlevel')]
        self._initdefaultvalue = portTab[_refTab.index('initvalue')]
        self._notsimudatacustom = portTab[_refTab.index('custom')]
        self._comment = portTab[_refTab.index('comment')]
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
