from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import csv

class ConnexionWrapper(QAbstractTableModel):



    def __init__(self, filename, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._thing = "cnw_wrapper"
        self._objectTab = []
        self._filename = filename

        _csvFile = open(self._filename, "r")

        #self._reader = csv.DictReader(_csvFile, delimiter=';')
        _reader = csv.reader(_csvFile, delimiter=';')

        for _line in _reader:
            self._objectTab.append(_line)

        self._headerData = self._objectTab[0]
        print(self._headerData)

    def _name(self):
        return str(self._thing)

    def rowCount(self, parent=None, *args, **kwargs):
        _rows = list(self._reader)
        return len(_rows)

    def columnCount(self, parent):
        return len(self._headerData)

    def roleNames(self):
        pass

    def data(self, QModelIndex, role=None):
        if role == QtCore.Qt.DisplayRole:
            _row = QModelIndex.row()
            _col = QModelIndex.column()
            _value = self._objectTab[_row][_col]
            return _value.name()
        else:
            return QtCore.QVariant()

    def rowCountlt(self):
        _rows = list(self._objectTab)
        return len(_rows)-1

    def flags(self, QModelIndex):
        return QtCore.Qr.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    def columnCountlt(self):
        return len(self._headerData)

    def datalt(self,row,col):
        return self._objectTab[row][col]