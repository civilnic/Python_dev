import re


class BDS:
    """
    Class to defined BDS data file containing A429 frame description (typically for EIS/SDAC/FWC systems)
    Return a BDS object containing:
        _ a dictionary of A429 label object (see A429 module)
        _ a dictionary of Discrete data object (not implemented yet i.e. not filled yet)
        _ a parameter object List (see A429 module)
        _ a dictionary of source i.e system exchanging label with system represented by BDS
    """

    def __init__(self):
        """
        No attributes are needed
        """
        self.A429LabelDict = dict()
        self.DisDict = dict()
        self.ParameterList = []
        self.sourceDict = dict()


    def add_Label(self, LabelOject):
        """
        Add a label object into BDS storage dictionary
        Labels are stored with their identifier in dictionary.
        The identifier is a tuple made of the following fields
            self.nature, self.system, self.number, self.sdi,self.source

        Return label object added in dictionary
        """
        #create the label identifier
        labelIdentifier=LabelOject.createIndentifier()

        # if identifier not in BDS dict
        # if identifier already in BDS => don't do anything
        if(labelIdentifier not in self.A429LabelDict.keys()):

            # add label into dictionary
            self.A429LabelDict[labelIdentifier] = LabelOject
            pass

        return self.A429LabelDict[labelIdentifier]

    def add_Parameter(self, ParamOject):
        """
        Add a parameter object into BDS parameter list
        :param ParamOject: parameter object to add
        :return None:
        """
        self.ParameterList.append(ParamOject)

    def get_ParameterList(self):
        """
        Get the BDS list of parameter object
        :return: list of parameter object
        """
        return self.ParameterList

    def add_Source(self, source):
        """
        Add a source into BDS dict
        :param source:
        :return:
        """
        # add source if not already in dict
        if (source not in self.sourceDict):
            self.sourceDict[source] = source

    def get_LabelObjList(self, **paramdict):
        """
        Get a Label Object list depending on sereval criteria set by label **paramdict
        nature/system/number/sdi/source
        :param paramdict:
        :return label Oject list:
        """

        # self.nature, self.system, self.number, self.sdi,self.source
        mylabellist = []

        if 'nature' in paramdict:
            naturesearched = str(paramdict['nature'])
        else:
            naturesearched = ".*"

        if 'system' in paramdict:
            systemsearched = str(paramdict['system'])
        else:
            systemsearched = ".*"

        if 'number' in paramdict:
            numbersearched = str(paramdict['number'])
        else:
            numbersearched = ".*"

        if 'sdi' in paramdict:
            sdisearched = str(paramdict['sdi'])
        else:
            sdisearched = ".*"

        if 'source' in paramdict:
            sourcesearched = str(paramdict['source'])
        else:
            sourcesearched = ".*"

        natureregexp = re.compile(naturesearched)
        systemregexp = re.compile(systemsearched)
        numberregexp = re.compile(numbersearched)
        sdiregexp = re.compile(sdisearched)
        sourceregexp = re.compile(sourcesearched)

        for (nature, system, number, sdi, source) in sorted(self.A429LabelDict.keys()):
            if natureregexp.search(str(nature)):
                if systemregexp.search(str(system)):
                    if numberregexp.search(str(number)):
                        if sdiregexp.search(str(sdi)):
                            if sourceregexp.search(str(source)):
                                mylabellist.append(self.A429LabelDict[(nature, system, number, sdi, source)])
        return mylabellist


    def ComputeResolutionBCD(self, nb_bits, range):
        """
        Compute resolution for a BCD label from number of bits used and range
        :param nb_bits:
        :param range:
        :return resolution:
        """

        max_encoding = 0.0
        n_digit = 0
        nombre_bits=int(nb_bits)

        if len(re.findall("\s", str(range))) > 0:
            range_chaine = range.split(" ")
            range = float(range_chaine[-1])
        else:
            range = float(range)

        while nombre_bits > 3:
            max_encoding = max_encoding + 9*10**n_digit
            nombre_bits -= 4
            n_digit += 1
        if nombre_bits == 3:
            max_encoding = max_encoding + 7*10**n_digit
        elif nombre_bits == 2:
            max_encoding = max_encoding + 3*10**n_digit
        elif nombre_bits == 1:
            max_encoding = max_encoding + 1*10**n_digit

        resolution = "%.10f" % (float(range) / max_encoding)

        return resolution

    def ComputeResolutionBNR(self, nb_bits, range):
        """
        Compute resolution for a BNR label from number of bits used and range
        :param nb_bits:
        :param range:
        :return resolution:
        """
        nombre_bits=int(nb_bits)

        if nombre_bits > 0:
            resolution = "%.10f" % (float(range) / (2 ** nombre_bits))
        else:
            resolution = None

        return resolution