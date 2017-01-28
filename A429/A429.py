import re

class A429Label:
    """
    Class to defined A429Label data
    """

    def __init__(self, number, sdi, labeltype, nature, system):
        """
        Attributes are:
        _ path name of the file
        """
        self.number = int(number)
        self.sdi = convertSDI(sdi)
        self.labeltype = labeltype
        self.system = system
        self._nature = convertNature(nature)
        self._source = None
        self._ssmtype = None
        self._originATA = None
        self._input_trans_rate = None
        self._pins = None
        self._LinkToInput = None
        self.SimuFormattedName = None
        self.ParameterList = []

    @property
    def ssmtype(self):
        if self.labeltype == "BNR":
            self._ssmtype = "BNR"
        elif self.labeltype == "DW":
            self._ssmtype = "DW"
        elif self.labeltype == "BCD":
            self._ssmtype = "BCD"
        elif self.labeltype == "HYB":
            # we parse parameters list of current label
            # if one parameter is BNR => status will be BNR type
            # if one parameter is BCD => status will be BCD type
            # else status is set to default value: no SSM
            if self.ParameterList:
                for paramobj in self.ParameterList:
                    if paramobj.formatparam == "BNR":
                        self._ssmtype = "BNR"
                        break
                    elif paramobj.formatparam == "BCD":
                        self._ssmtype = "BCD"
                        break
                    else:
                        self._ssmtype = ""
                    pass
            else:
                self._ssmtype = ""
        else:
            self._ssmtype = ""

        return self._ssmtype

    @ssmtype.setter
    def ssmtype(self, ssmtype):
        self._ssmtype = ssmtype

    @property
    def LinkToInput(self):
        return self._LinkToInput
    @LinkToInput.setter
    def LinkToInput(self, LinkToInput):
        self._LinkToInput = LinkToInput

    @property
    def nature(self):
        return self._nature
    @nature.setter
    def nature(self, nature):
        self._nature = convertNature(nature)

    @property
    def originATA(self):
        return self._originATA
    @originATA.setter
    def originATA(self, originATA):
        self._originATA = originATA

    @property
    def input_trans_rate(self):
        return self._input_trans_rate

    @input_trans_rate.setter
    def input_trans_rate(self, input_trans_rate):
        self._input_trans_rate = input_trans_rate

    @property
    def pins(self):
        return self._pins
    @pins.setter
    def pins(self, pins):
        self._pins = pins

    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, source):
        self._source = source

    def refParameter(self, paramObj):
        self.ParameterList.append(paramObj)
        paramObj.labelObj = self

    def getParameterList(self):
        return self.ParameterList

    def print(self, DisplayParam):
        print ("Label number: "+str(self.number))
        print ("\tLabel sdi: "+str(self.sdi))
        print ("\tLabel type: "+str(self.labeltype))
        print ("\tLabel of system: "+str(self.system))
        print ("\tLabel source: "+str(self._source))
        print ("\tLabel pins: "+str(self.pins))
        print ("\tLabel nature: "+str(self.nature))
        print ("\tLabel _ssmtype: "+str(self._ssmtype))
        print ("\tLabel SimuFormattedName: "+str(self.SimuFormattedName))
        if(DisplayParam is True):
            for param in self.getParameterList():
                param.print()

    def createIndentifier(self):

        """" create a unique label identifer to store on BDS label dictionary """

        identifier = (self.nature, self.system, self.number, str(self.sdi), self.source)
        return identifier


    def computeSsmType(self):

        """" compute attribute ssmtype if not attribute is not set """

        if not self.ssmtype:

            if self.labeltype == "BNR":
                self.ssmtype = "status_ssm_bnr"
            elif self.labeltype == "DW":
                self.ssmtype = "status_ssm_dis"
            elif self.labeltype == "BCD":
                self.ssmtype = "status_ssm_bcd"
            elif self.labeltype == "HYB":
                # we parse parameters list of current label
                # if one parameter is BNR => status will be BNR type
                # if one parameter is BCD => status will be BCD type
                # else status is set to default value: no SSM
                for paramobj in self.ParameterList:
                    if paramobj.formatparam == "BNR":
                        self.ssmtype = "status_ssm_bnr"
                        break
                    elif paramobj.formatparam == "BCD":
                        self.ssmtype = "status_ssm_bcd"
                        break
                    else:
                        self.ssmtype = "status_no_ssm"
                    pass
            else:
                self.ssmtype = "status_no_ssm"


class A429Parameter:
    """
    Base class to defined A429 signal type
    """

    def __init__(self, name, nature,label):
        self.name = name
        self.nature = convertNature(nature)
        self.label = int(label)
        self._codingtype = None
        self._unit = None
        self._comments = None
        self._formatparam = None
        self._parameter_def = None
        self._nombloc = None
        self._libbloc = None
        self._labelObj = None
        self.SimuPreFormattedName = None

    @property
    def formatparam(self):
        return self._formatparam
    @formatparam.setter
    def formatparam(self, formatparam):
        self._formatparam = formatparam

    @property
    def labelObj(self):
        return self._labelObj
    @labelObj.setter
    def labelObj(self, labelObj):
        self._labelObj = labelObj

    @property
    def libbloc(self):
        return self._libbloc
    @libbloc.setter
    def libbloc(self, libbloc):
        self._libbloc = libbloc

    @property
    def nombloc(self):
        return self._nombloc
    @nombloc.setter
    def nombloc(self, nombloc):
        self._nombloc = nombloc

    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, unit):
        self._unit = unit

    @property
    def comments(self):
        return self._comments
    @comments.setter
    def comments(self, comments):
        self._comments = comments

    @property
    def parameter_def(self):
        return self._parameter_def
    @parameter_def.setter
    def parameter_def(self, parameter_def):
        self._parameter_def = parameter_def

    @property
    def codingtype(self):
        return self._codingtype
    @codingtype.setter
    def codingtype(self, codingtype):
        self._codingtype = codingtype

    @property
    def signed(self):
        return self._signed
    @signed.setter
    def signed(self, signed):

        convert_sign = str(signed)

        if signed:
            if (convert_sign == "yes") or (convert_sign =="O"):
                self._signed = "1"
            elif (convert_sign == "no") or (convert_sign =="N"):
                self._signed = "0"
            elif convert_sign == "True":
                self._signed = "1"
            else:
                self._signed = "0"
        else:
            self._signed = "0"

    def print(self):
        print("\t\tParameter name: " + str(self.name))
        print("\t\t\tParameter nature: " + str(self.nature))
        print("\t\t\tParameter codingtype: " + str(self._codingtype))
        print("\t\t\tParameter unit: " + str(self._unit))
        print("\t\t\tParameter commment: " + str(self._comments))
        print("\t\t\tParameter parameter_def: " + str(self.parameter_def))



class A429ParamDIS(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Parameter.__init__(self, name, nature, label)

        self.codingtype = "boolean"
        self._BitNumber = None
        self._state0 = None
        self._state1 = None
        self.nb_bits = 1
        self.lsb = None
        self.msb = None
        self.signed = "0"


    @property
    def BitNumber(self):
        return self._BitNumber
    @BitNumber.setter
    def BitNumber(self, BitNumber):
        self._BitNumber = int(BitNumber)
        self.lsb = int(BitNumber)
        self.msb = int(BitNumber)

    @property
    def state0(self):
        return self._state0
    @state0.setter
    def state0(self, state0):
        self._state0 = state0

    @property
    def state1(self):
        return self._state1
    @state1.setter
    def state1(self, state1):
        self._state1 = state1

    def print(self):
        super(A429ParamDIS, self).print()
        print("\t\t\tParameter BitNumber: " + str(self.BitNumber))
        print("\t\t\tParameter state0: " + str(self.state0))
        print("\t\t\tParameter state1: " + str(self.state1))

class A429ParamBNR(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label, msb, nb_bits, range, resolution):
        A429Parameter.__init__(self,name, nature, label)
        self.codingtype = "float"
        self.msb = int(msb)
        self.nb_bits = int(nb_bits)
        self.range = float(range)
        self.resolution = float(resolution)
        self.lsb = int(self.msb) - int(self.nb_bits) + 1
        self._accuracy = None
        self._signed = "1"

    @property
    def accuracy(self):
        return self._accuracy
    @accuracy.setter
    def accuracy(self, accuracy):
        if(accuracy):
            if isfloat(accuracy):
                self._accuracy = float(accuracy)
            else:
                self.accuracy = None

    def print(self):
        super(A429ParamBNR, self).print()
        print("\t\t\tParameter msb: " + str(self.msb))
        print("\t\t\tParameter nb_bits: " + str(self.nb_bits))
        print("\t\t\tParameter range: " + str(self.range))
        print("\t\t\tParameter resolution: " + str(self.resolution))
        print("\t\t\tParameter lsb: " + str(self.lsb))
        print("\t\t\tParameter accuracy: " + str(self.accuracy))
        print("\t\t\tParameter signed: " + str(self.signed))


class A429ParamBCD(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label, msb, nb_bits, range, resolution):
        A429Parameter.__init__(self,name, nature, label)
        self.codingtype = "int"
        self.msb = int(msb)
        self.nb_bits = int(nb_bits)
        self.lsb = int(self.msb) - int(self.nb_bits) + 1
        self.signed = "0"

        if len(re.findall("\s", range)) > 0:
            range_chaine = range.split(" ")
            self.range = float(range_chaine[-1])
        else:
            self.range = float(range)

        self.resolution = float(resolution)

    def print(self):
        super(A429ParamBCD, self).print()
        print("\t\t\tParameter msb: " + str(self.msb))
        print("\t\t\tParameter nb_bits: " + str(self.nb_bits))
        print("\t\t\tParameter range: " + str(self.range))
        print("\t\t\tParameter resolution: " + str(self.resolution))

class A429ParamOpaque(A429Parameter):
    """
    Base class to defined A429 Opaque parameter type
    """

    def __init__(self, name, nature, label, msb, nb_bits):
        A429Parameter.__init__(self, name, nature, label)
        self.codingtype = "int"
        self.msb = int(msb)
        if nb_bits:
            self.nb_bits = int(nb_bits)
            self.lsb = int(self.msb) - int(self.nb_bits) + 1
        else:
            self.nb_bits = None
            self.lsb = "1"


        self.signed = "0"

    def print(self):
        super(A429ParamOpaque,self).print()
        print("\t\t\tParameter msb: " + str(self.msb))
        print("\t\t\tParameter nb_bits: " + str(self.nb_bits))


class A429ParamISO5(A429Parameter):
    """
    Base class to defined A429 ISO5 parameter type
    """

    def __init__(self, name, nature, label, msb, nb_bits):
        A429Parameter.__init__(self, name, nature, label)
        self.codingtype = "char"
        self.msb = int(msb)
        if(nb_bits):
            self.nb_bits = int(nb_bits)
            self.lsb = int(self.msb) - int(self.nb_bits) + 1
        else:
            self.nb_bits = None


    def print(self):
        super(A429ParamISO5,self).print()
        print("\t\t\tParameter msb: " + str(self.msb))
        print("\t\t\tParameter nb_bits: " + str(self.nb_bits))



def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False

def convertNature(nature):
    if nature == 'O':
        nature = "OUT"
    elif nature == "I":
        nature = "IN"
    elif nature == "ENTREE":
        nature = "IN"
    elif nature == "SORTIE":
        nature = "OUT"
    else:
        return None

    return nature

def convertSDI(sdi):

    # set formatted name (i.e simulation label name)pip
    try:
        # we test here if string can be interpreded as an integer
        _sdi = int(sdi, 2)

        # string convertion
        _sdi = str(_sdi)

        # test cases
        if (_sdi == "0") or (_sdi == "00"):
            _sdi = "00"
        elif (_sdi == "1") or (_sdi == "01"):
            _sdi = "01"
        elif (_sdi == "10") or (_sdi == "2"):
            _sdi = "10"
        elif (_sdi == "11") or (_sdi == "3"):
            _sdi = "11"

    except ValueError:
        _sdi = str(sdi)

    return _sdi