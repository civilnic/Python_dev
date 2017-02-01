import re


class BDS:
    """
    Class to defined BDS data file
    """

    def __init__(self):
        """
        Attributes are:
        _ path name of the file
        """
        self.A429LabelDict = dict()
        self.DisDict = dict()
        self.ParameterList = []
        self.sourceDict = dict()


    def add_Label(self, LabelOject):

        # an label identifier is a tuple made of the following fields
        # self.nature, self.system, self.number, self.sdi,self.source
        labelIdentifier=LabelOject.createIndentifier()
        if(labelIdentifier not in self.A429LabelDict.keys()):
            self.A429LabelDict[labelIdentifier] = LabelOject
            pass
            #print("Label deja dans la BDS: " + str(labelIdentifier))
        return self.A429LabelDict[labelIdentifier]

    def add_Parameter(self, ParamOject):
        self.ParameterList.append(ParamOject)

    def get_ParameterList(self):
        return self.ParameterList

    def add_Source(self, source):
        if (source not in self.sourceDict):
            self.sourceDict[source] = source

    def get_LabelObjList(self, **paramdict):

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
            print("numbersearched: " + numbersearched)
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

        nombre_bits=int(nb_bits)

        if nombre_bits > 0:
            resolution = "%.10f" % (float(range) / (2 ** nombre_bits))
        else:
            resolution = None

        return resolution