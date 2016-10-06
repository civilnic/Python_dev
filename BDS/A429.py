class A429Label:
    """
    Class to defined A429Label data
    """

    def __init__(self, number, sdi,labetype,nature):
        """
        Attributes are:
        _ path name of the file
        """
        self.number = number
        self.sdi = sdi
        self.labetype = labetype
        self.nature = nature
        self._source = None
        self._originATA = None
        self._input_trans_rate = None
        self._pins = None
        self._LinkToInput = None
        self.signalList = []

    def _set_LinkToInput(self, LinkToInput):
        self._LinkToInput = LinkToInput
    def _get_LinkToInput(self):
        return self._LinkToInput
    LinkToInput = property(_get_LinkToInput, _set_LinkToInput)


    def _set_nature(self, nature):
        self._nature = nature
    def _get_nature(self):
        return self._nature
    nature = property(_get_nature, _set_nature)

    def _set_originATA(self,origin_ATA):
        self._originATA=origin_ATA
    def _get_originATA(self):
        return self._originATA
    originATA = property(_get_originATA,_set_originATA)

    def _set_input_trans_rate(self, input_trans_rate):
        self._originATA = input_trans_rate
    def _get_input_trans_rate(self):
        return self._input_trans_rate
    input_trans_rate = property(_get_input_trans_rate, _set_input_trans_rate)


    def _set_pins(self, pins):
        self._pins = pins
    def _get_pins(self):
        return self._pins
    pins = property(_get_pins, _set_pins)


    def _set_source(self, source):
        self._source = source
    def _get_source(self):
        return self._source
    source = property(_get_source, _set_source)

    def addSignal(self,signalObj):
        self.signalList.append(signalObj)


class A429Parameter:
    """
    Base class to defined A429 signal type
    """

    def __init__(self, name, nature,label):
        self.name = name
        self.nature = nature
        self.label = label
        self._codingtype = None
        self._unit = None
        self._comments = None
        self._parameter_def = None

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


class A429ParamDIS(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Parameter.__init__(self,name, nature, label)

        self.codingtype="boolean"
        self._BitNumber=None
        self._state0=None
        self._state1=None

        @property
        def BitNumber(self):
            return self._BitNumber
        @BitNumber.setter
        def BitNumber(self, BitNumber):
            self._BitNumber = BitNumber

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

class A429ParamBNR(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label, msb, nb_bits, range, resolution):
        A429Parameter.__init__(self,name, nature, label)
        self.codingtype="float"
        self.msb = msb
        self.nb_bits = nb_bits
        self.range = range
        self.resolution = resolution
        self.lsb = self.msb - self.nb_bits
        self._accuracy = None
        self._signed = None

    @property
    def accuracy(self):
        return self._accuracy
    @accuracy.setter
    def accuracy(self, accuracy):
        self._accuracy = accuracy


    @property
    def signed(self):
        return self._signed
    @signed.setter
    def signed(self, signed):
        self._signed = signed

class A429ParamBCD(A429Parameter):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label, msb, signif_bits, range, resolution):
        A429Parameter.__init__(self,name, nature, label)
        self.codingtype="float"
        self.msb = msb
        self.signif_bits = signif_bits
        self.range = range
        self.resolution = resolution