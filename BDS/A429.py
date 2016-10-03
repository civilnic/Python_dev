class A429Label:
    """
    Class to defined A429Label data
    """

    def __init__(self, number, sdi):
        """
        Attributes are:
        _ path name of the file
        """
        self.number = number
        self.sdi = sdi
        self._nature = None
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

class A429LabelBNR(A429Label):
    """
    Class to defined A429Label of BNR type (herits from A429_Label class)
    """

    def __init__(self,number,sdi,signif_bits,range,resolution):
        A429Label.__init__(self,number,sdi)
        self.type = "BNR"
        self.signif_bits = signif_bits
        self.range = range
        self.resolution = resolution
        self._accuracy=None

    def _set_accuracy(self, accuracy):
        self._accuracy = accuracy
    def _get_accuracy(self):
        return self._accuracy
    accuracy = property(_get_accuracy, _set_accuracy)


class A429LabelBCD(A429LabelBNR):
    """
    Class to defined A429Label of BCD type (herits from A429_Label class)
    """

    def __init__(self, number,sdi,signif_bits,range,resolution):
        A429LabelBNR.__init__(self,number,sdi,signif_bits,range,resolution)
        self.type = "BCD"



class A429LabelHYB(A429LabelBNR):
    """
    Class to defined A429Label of HYB type (herits from A429_Label class)
    """

    def __init__(self, number,sdi,signif_bits,range,resolution):
        A429LabelBNR.__init__(self,number,sdi,signif_bits,range,resolution)
        self.type = "HYB"

class A429LabelDIS(A429Label):
    """
    Class to defined A429Label of DIS type (herits from A429_Label class)
    """
    def __init__(self,number,sdi):
        A429Label.__init__(self,number,sdi)
        self.type = "DIS"



class A429Signal:
    """
    Base class to defined A429 signal type
    """

    def __init__(self, name, nature,label):
        self.name = name
        self.nature = nature
        self.label = label
        self._type = None
        self._unit = None
        self._comments = None
        self._parameter_def = None

    def _set_unit(self, unit):
        self._unit = unit
    def _get_unit(self):
        return self._unit
    unit = property(_get_unit, _set_unit)


    def _set_comments(self, comments):
        self._comments = comments
    def _get_comments(self):
        return self._comments
    comments = property(_get_comments, _set_comments)

    def _set_parameter_def(self, parameter_def):
        self._parameter_def = parameter_def
    def _get_parameter_def(self):
        return self._parameter_def
    parameter_def = property(_get_parameter_def, _set_parameter_def)


    def _set_type(self, type):
        self._type = type
    def _get_type(self):
        return self._type
    type = property(_get_type, _set_type)


class A429SignalBool(A429Signal):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Signal.__init__(self,name, nature, label)

        self.type="boolean"
        self._BitNumber=None
        self._state0=None
        self._state1=None


        def _set_BitNumber(self, BitNumber):
            self._BitNumber = BitNumber
        def _get_BitNumber(self):
            return self._BitNumber
        BitNumber = property(_get_BitNumber, _set_BitNumber)


        def _set_state0(self, state0):
            self._state0 = state0
        def _get_state0(self):
            return self._state0
        state0 = property(_get_state0, _set_state0)


        def _set_state1(self, state1):
            self._state1 = state1
        def _get_state1(self):
            return self._state1
        state1 = property(_get_state1, _set_state1)
        

class A429SignalFloat(A429Signal):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Signal.__init__(self,name, nature, label)
        self.type="float"