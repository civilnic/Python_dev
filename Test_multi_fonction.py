import sys

from BDS.BDS2XML import BDS2XML
from BDS.BDS_EIS import BDS_EIS
from BDS.BDS_FWC import BDS_FWC
from FDEF.FDEF_XML import FDEF_XML
from MICD.MICD import MICD
from MICD.MICD import MICD_port

def AddLabelToMICD(micdFile, labelObj):

    # compute nature field "IN/OUT" in fdef MICD
    # the nature in MICD is the opposite of nature in BDS
    # IN => OUT ,  OUT => IN
    if labelObj.nature == "IN":
        _micdPortType = "OUT"
    else:
        _micdPortType = "IN"

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
    _micdPort.fromto = "from: "+str(labelObj.source)+" to FWC"
    _micdPort.interfacelevel = "format"

    # add label data to MICD
    micdFile.AddPortfromPortObject(_micdPort)

    # associated port corresponding to label refresh
    _micdPort.description = "refresh of Label: " + str(_micdPort.name)
    _micdPort.name = _micdPort.name+"_R"
    _micdPort.codingtype = "boolean"
    _micdPort.convention = ""
    _micdPort.status = "True"

    # add refresh data to MICD
    micdFile.AddPortfromPortObject(_micdPort)

    # invert micd port type to write preformatted data
    if _micdPortType == "IN":
        _micdPortType = "OUT"
    else:
        _micdPortType = "IN"
    _micdPort.type = _micdPortType
    _micdPort.name = labelObj.SimuFormattedName+"_SSM"
    _micdPort.codingtype = "int"
    _micdPort.comformat = "ENV"
    _micdPort.description = "SSM of Label: " + str(labelObj.SimuFormattedName)
    _micdPort.convention = "0:NO/2:NE/4:NCD/8:FW"
    _micdPort.fromto = str(labelObj.source)
    _micdPort.interfacelevel = "preformat"

    # add refresh data to MICD
    micdFile.AddPortfromPortObject(_micdPort)

    for parameterObj in labelObj.getParameterList():
        AddParameterToMICD(micdFile, parameterObj)

    return True



def AddParameterToMICD(micdFile, ParameterObj):

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


    if _labelObj.labeltype == "DW":
        _micdPort.convention = _micdPort.convention+"\n bit position: "+str(ParameterObj.BitNumber)

    else:
        _micdPort.convention = _micdPort.convention + "\n number of bits: " + str(ParameterObj.nb_bits)

        if ParameterObj.formatparam != "DW":
            _micdPort.convention = _micdPort.convention + "\n msb: " + str(ParameterObj.msb)

        if _labelObj.labeltype != "ISO5" and ParameterObj.formatparam != "DW":
            _micdPort.convention = _micdPort.convention + "\n signed: " + ParameterObj.signed
            if hasattr(ParameterObj, "range"):
                _micdPort.convention = _micdPort.convention + "\n range: " + str(ParameterObj.range)

    micdFile.AddPortfromPortObject(_micdPort)

    return True





def main():

    print(sys.argv[1])

    bdsFWC = BDS_FWC(sys.argv[1], sys.argv[5])
    bds2xml_file = BDS2XML(sys.argv[2],True)
    bdsEis = BDS_EIS(sys.argv[3],sys.argv[4])

    print ("**EIS**")
    xml_file = FDEF_XML("test.xml", "A429")
    micdFile = MICD("FDEF.xls", "fdef_FWC", 'V1.0', True)

    labelObjList = bdsFWC.get_LabelObjList(nature="IN", system="FWC")

    for labelObj in labelObjList:
        if len(labelObj.ParameterList) > 0:

            AddLabelToMICD(micdFile, labelObj)

            xml_file.AddLabel(labelObj)
            for parameterObj in labelObj.getParameterList():
                bds2xml_file.AddLine(parameterObj)

    bds2xml_file.savefile()
    xml_file.WriteAndClose()
    micdFile.savefile()

main()


