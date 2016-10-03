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

    def _set_nature(self, nature):
        self._nature = nature

    def _get_nature(self, nature):
        return self._nature

    nature = property(_get_nature, _set_nature)

    def _set_originATA(self,origin_ATA):
        self._originATA=origin_ATA

    def _get_originATA(self,origin_ATA):
        return self._originATA

    originATA = property(_get_originATA,_set_originATA)

    def _set_input_trans_rate(self, input_trans_rate):
        self._originATA = input_trans_rate

    def _get_input_trans_rate(self, input_trans_rate):
        return self._input_trans_rate

    input_trans_rate = property(_get_input_trans_rate, _set_input_trans_rate)


    def _set_pins(self, pins):
        self._pins = pins

    def _get_pins(self, pins):
        return self._pins

    pins = property(_get_pins, _set_pins)


    def _set_source(self, source):
        self._source = source

    def _get_source(self, source):
        return self._source

    source = property(_get_source, _set_source)



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
    def _get_accuracy(self, accuracy):
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
        self.type = None
        self.label = label
        self.comments = None
        self.parameter_def = None

    def _set_comments(self, comments):
        self._comments = comments
    def _get_comments(self, comments):
        return self._comments
    comments = property(_get_comments, _set_comments)

    def _set_parameter_def(self, parameter_def):
        self._parameter_def = parameter_def
    def _get_parameter_def(self, parameter_def):
        return self._parameter_def
    parameter_def = property(_get_parameter_def, _set_parameter_def)


    def _set_type(self, type):
        self._type = type
    def _get_type(self, type):
        return self._type
    type = property(_get_type, _set_type)


class A429SignalBool(A429Signal):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Signal.__init__(self,name, nature, label)
        self._set_type("boolean")

class A429SignalFloat(A429Signal):
    """
    Base class to defined A429 BOOL signal type
    """

    def __init__(self, name, nature, label):
        A429Signal.__init__(self,name, nature, label)
        self._set_type("float")