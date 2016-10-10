import re

class A429Label:
    """
    Class to defined A429Label data
    """

    def __init__(self, number, sdi,labeltype,nature,system):
        """
        Attributes are:
        _ path name of the file
        """
        self.number = int(number)
        self.sdi = sdi
        self.labeltype = labeltype
        self.system = system
        self._source = None
        self._ssmtype = None
        self._originATA = None
        self._input_trans_rate = None
        self._pins = None
        self._LinkToInput = None
        self.SimuFormattedName = None
        self.ParameterList = []

        self.nature = convertNature(nature)

    @property
    def ssmtype(self):
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
        self._nature = nature

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
        #print (self.number)
        self.ParameterList.append(paramObj)
        paramObj.labelObj = self

        if self.number==271:

            for param in self.ParameterList:
                pass
                #print(paramObj.name)



    def getParameterList(self):
        return self.ParameterList

    def print(self, DisplayParam):
        print ("Label number: "+str(self.number))
        print ("\tLabel sdi: "+str(self.sdi))
        print ("\tLabel type: "+str(self.labeltype))
        print ("\tLabel of system: "+str(self.system))
        print ("\tLabel source: "+str(self._source))
        print ("\tLabel nature: "+str(self.nature))
        print ("\tLabel _ssmtype: "+str(self._ssmtype))
        if(DisplayParam is True):
            for param in self.getParameterList():
                param.print()

    def createIndentifier(self):
        identifier = (self.nature, self.system, self.number, self.sdi,self.source)
        return identifier


class A429Parameter:
    """
    Base class to defined A429 signal type
    """

    def __init__(self, name, nature,label):
        self.name = name
        self.nature = nature
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


    @property
    def BitNumber(self):
        return self._BitNumber
    @BitNumber.setter
    def BitNumber(self, BitNumber):
        self._BitNumber = int(BitNumber)


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
        self.codingtype="float"
        self.msb = int(msb)
        self.nb_bits = int(nb_bits)
        self.range = float(range)
        self.resolution = float(resolution)
        self.lsb = int(self.msb) - int(self.nb_bits)
        self._accuracy = None
        self._signed = None

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

    @property
    def signed(self):
        return self._signed
    @signed.setter
    def signed(self, signed):
        self._signed = signed


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

        if len(re.findall("\s", range))> 0:
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
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label, msb, nb_bits):
        A429Parameter.__init__(self, name, nature, label)
        self.codingtype = "int"
        self.msb = int(msb)
        if(nb_bits):
            self.nb_bits = int(nb_bits)
        else:
            self.nb_bits = None


    def print(self):
        super(A429ParamOpaque,self).print()
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