import csv
import re
import xlrd
import os

class mexico_coupling:

    """
    Class to parse and analyze mexico coupling files
    """
    fieldnames = ['ICD Name', 'Signal Name', ' Last Modification', ' Comment', ' Sheet Name']

    def __init__(self, pathname):

        self._pathname = pathname

        _fileName, _fileExtension = os.path.splitext(pathname)

        if (_fileExtension == ".xls") or (_fileExtension == ".xlsx"):
            self._type = "XLS"
        elif (_fileExtension == ".csv"):
            self._type = "CSV"
        else:
            self._type = "Unknown"

        self._aliasObjList = []

        self.parse()

    @property
    def pathname(self):
        return self._pathname

    @pathname.setter
    def pathname(self, pathname):
        self._pathname = pathname

    def addaliasObj(self, aliasObj):
        if aliasObj not in self._aliasObjList:
            self._aliasObjList.append(aliasObj)

    def getAliasObj(self):
        return self._aliasObjList

    def parse(self):

        if self._type == "CSV":

            _file = open(self._pathname, "r")

            try:
                #
                # Use ''DictReader'' to directly have a dictionary (keys are the first row value)
                #
                reader = csv.DictReader(_file, delimiter=';')

                #
                # read data
                #
                for _row in reader:
                    self.ParseCSVLine(_row)

            finally:
                _file.close()

    def ParseCSVLine(self, row):

        aliasObj = Alias(row[mexico_coupling.fieldnames[0]],
                         row[mexico_coupling.fieldnames[1]],
                         row[mexico_coupling.fieldnames[4]],
                         row[mexico_coupling.fieldnames[3]],
                         row[mexico_coupling.fieldnames[2]]
                         )
        self.addaliasObj(aliasObj)



    def write(self):

        with open(self._pathname, 'w', newline='') as _csvfile:

            # output file header
            fieldnames = mexico_coupling.fieldnames
            writer = csv.DictWriter(_csvfile, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()

            for _aliasObj in self.getAliasObj():
                writer.writerow(_aliasObj.getAliasLineDict())

        _csvfile.close()

class Alias:

    """
    Class to extract information on a coupling file line
    """
    # a coupling file line is defined by:
    #   ICD Name;	Signal Name;	Last Modification;	Comment;	Sheet Name;

    def __init__(self, portname, channelname, sheetName, comment=None, date=None):

        # port concerning by alias
        self._portname = portname

        # regexp to test Signal Name field:
        # the field can have the following format:
        # signal_name
        # signal_name#operator
        # signal_name[indice]
        # signal_name{indice]#operator

        _testOnSignal = re.match(r'(?P<signal_name>\w+)(?:\[(?P<indice>\d+)\])*(?:#(?P<operator>\w+))*', channelname)

        if _testOnSignal:
            self._signal = _testOnSignal.group("signal_name")
            self._indice = _testOnSignal.group("indice")
            self._operator = _testOnSignal.group("operator")

        self._sheetname = sheetName

        _testOnSheetNameFUNIN = re.match(r'(FUN(_\w+)*_IN)', sheetName)
        _testOnSheetNameFUNOUT = re.match(r'(FUN(_\w+)*_OUT)', sheetName)
        # sheet name match *_IN => it's a FUN_IN sheet name
        # this test is usefull in case of multiple input port sheets
        if _testOnSheetNameFUNIN:
            self._portype = "consumer"
        elif _testOnSheetNameFUNOUT:
            self._portype = "producer"
        else:
            self._portype = None

        self._date = date
        self._comment = comment

    def hasOperator(self):
        if self.operator:
            return True
        else:
            return False

    def hasIndice(self):
        if self.indice:
            return True
        else:
            return False

    def getAliasLineDict(self):

        if self.indice and self.operator:
            _signalName = self.signal+"["+str(self.indice)+"]#"+self.operator
        elif self.indice and not self.operator:
            _signalName = self.signal+"["+str(self.indice)+"]"
        elif not self.indice and self.operator:
            _signalName = self.signal+"#"+self.operator
        else:
            _signalName = self.signal

        _dict = {mexico_coupling.fieldnames[0]: self.portname,
                 mexico_coupling.fieldnames[1]: _signalName,
                 mexico_coupling.fieldnames[2]: self.date,
                 mexico_coupling.fieldnames[3]: self.comment,
                 mexico_coupling.fieldnames[4]: self.sheetname,
                 }
        return _dict

    @property
    def portname(self):
        return self._portname

    @portname.setter
    def portname(self, portname):
        self._portname = portname

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, signal):
        self._signal = signal

    @property
    def indice(self):
        return self._indice

    @indice.setter
    def indice(self, indice):
        self._indice = indice

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, operator):
        self._operator = operator

    @property
    def sheetname(self):
        return self._sheetname

    @sheetname.setter
    def sheetname(self, sheetname):
        self._sheetname = sheetname

    @property
    def portype(self):
        return self._portype

    @portype.setter
    def portype(self, portype):
        self._portype = portype

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment