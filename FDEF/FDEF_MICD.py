from MEXICO.MICD.MICD import MICD
from MEXICO.MICD.MICD import MICD_port
from A429.A429 import (A429Label, A429ParamDIS, A429ParamBNR, A429ParamBCD, A429ParamOpaque, A429ParamISO5)


class FDEF_MICD(MICD):
    """
    Base class to create MICD for FDEF model
    """

    def __init__(self, pathname, modelname=None, modelversion=None, deformat=False):
        MICD.__init__(self, pathname, modelname, modelversion, True)
        self._deformat = deformat

    @property
    def deformat(self):
        return self._deformat
    @deformat.setter
    def deformat(self, deformat):
        self._deformat = deformat

    def AddLabelToMICD(self, labelObj):

        # compute nature field "IN/OUT" in fdef MICD
        # the nature in MICD is the opposite of nature in BDS
        # IN => OUT ,  OUT => IN
        if not self._deformat:
            if labelObj.nature == "IN":
                _micdPortType = "OUT"
                _sheet_name = "FUN_OUT"
            else:
                _micdPortType = "IN"
                _sheet_name = "FUN_IN"
        else:
            if labelObj.nature == "IN":
                _micdPortType = "IN"
                _sheet_name = "FUN_IN"
            else:
                _micdPortType = "OUT"
                _sheet_name = "FUN_OUT"

        # port corresponding to label
        _micdPort = MICD_port(None, _micdPortType, None)
        _micdPort.name = labelObj.SimuFormattedName
        _micdPort.codingtype = "int"
        _micdPort.comformat = "A429"
        _micdPort.dim1 = 1
        _micdPort.dim2 = 1
        _micdPort.unit = "wu"
        _micdPort.description = "Label type: "+str(labelObj.labeltype)
        _micdPort.commode = "S"
        _micdPort.resfreshrate = 1
        _micdPort.prodconsif = "True"
        _micdPort.aircraftsignalname = "/not_available/"
        _micdPort.status = "False"
        _micdPort.simulationlevel = "True"
        _micdPort.notsimudatacustom = "False"
        _micdPort.convention = " sdi: "+str(labelObj.sdi)+"  ssm type: "+str(labelObj.ssmtype)
        _micdPort.fromto = str(labelObj.source)
        _micdPort.interfacelevel = "format"

        # add label data to MICD
        self.AddPortfromPortObject(_micdPort,_sheet_name)

        # associated port corresponding to label refresh
        _micdPort.description = "refresh of Label: " + str(_micdPort.name)
        _micdPort.name = _micdPort.name+"_R"
        _micdPort.codingtype = "boolean"
        _micdPort.convention = ""
        _micdPort.status = "True"

        # add refresh data to MICD
        self.AddPortfromPortObject(_micdPort,_sheet_name)

        # invert micd port type to write preformatted data
        if _micdPortType == "IN":
            _micdPortType = "OUT"
            _sheet_name = "FUN_OUT"
        else:
            _micdPortType = "IN"
            _sheet_name = "FUN_IN"
        _micdPort.type = _micdPortType
        _micdPort.name = labelObj.SimuFormattedName+"_SSM"
        _micdPort.codingtype = "int"
        _micdPort.comformat = "ENV"
        _micdPort.description = "SSM of Label: " + str(labelObj.SimuFormattedName)
        _micdPort.convention = "0:NO/2:NE/4:NCD/8:FW"
        _micdPort.fromto = str(labelObj.source)
        _micdPort.interfacelevel = "preformat"

        # add refresh data to MICD
        self.AddPortfromPortObject(_micdPort,_sheet_name)

        for parameterObj in labelObj.getParameterList():
            AddParameterToMICD(self, parameterObj,_sheet_name)

        return True


def AddParameterToMICD(micdFile,ParameterObj,sheet_name):

    # label object corresponding to parameter
    _labelObj = ParameterObj.labelObj

    # port corresponding to label
    _micdPort = MICD_port(None, ParameterObj.nature, None)
    _micdPort.name = ParameterObj.SimuPreFormattedName
    _micdPort.codingtype = ParameterObj.codingtype
    _micdPort.comformat = "ENV"
    _micdPort.dim1 = 1
    _micdPort.dim2 = 1
    _micdPort.unit = ParameterObj.unit
    _micdPort.description = ParameterObj.parameter_def
    _micdPort.commode = "S"
    _micdPort.resfreshrate = 1
    _micdPort.prodconsif = "True"
    _micdPort.aircraftsignalname = "/not_available/"
    _micdPort.status = "False"
    _micdPort.simulationlevel = "True"
    _micdPort.notsimudatacustom = "False"
    _micdPort.convention = "label type: "+str(_labelObj.labeltype)
    _micdPort.fromto = str(_labelObj.source)
    _micdPort.interfacelevel = "preformat"
    if ParameterObj.unit:
        _micdPort.unit = ParameterObj.unit
    else:
        _micdPort.unit = "wu"

    if isinstance(ParameterObj, A429ParamBNR) or isinstance(ParameterObj, A429ParamBCD):
        _micdPort.convention = _micdPort.convention + "\n number of bits: " + str(ParameterObj.nb_bits)
        _micdPort.convention = _micdPort.convention + "\n msb: " + str(ParameterObj.msb)
        _micdPort.convention = _micdPort.convention + "\n signed: " + ParameterObj.signed
        _micdPort.convention = _micdPort.convention + "\n range: " + str(ParameterObj.range)
    elif isinstance(ParameterObj, A429ParamDIS):
        _micdPort.convention = _micdPort.convention+"\n bit position: "+str(ParameterObj.BitNumber)
    elif isinstance(ParameterObj, A429ParamISO5) or isinstance(ParameterObj, A429ParamOpaque):
        _micdPort.convention = _micdPort.convention + "\n number of bits: " + str(ParameterObj.nb_bits)
        _micdPort.convention = _micdPort.convention + "\n msb: " + str(ParameterObj.msb)


    micdFile.AddPortfromPortObject(_micdPort, sheet_name)

    return True