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

    def rowCount(self, parent):
        _rows = list(self._reader)
        return len(_rows)

    def columnCount(self, parent):
        return len(self._headerData)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if not index.isValid():
                return QVariant()
            elif role != Qt.DisplayRole:
                return QVariant()
            _row = index.row()
            _col = index.column()
            return QVariant(self._objectTab[_row][_col])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headerData[col])
        if orientation == QtCore.Qt.Vertical:
            return ''

        return None

    def rowCountlt(self):
        _rows = list(self._objectTab)
        return len(_rows)-1


    def columnCountlt(self):
        return len(self._headerData)

    def datalt(self,row,col):
        return self._objectTab[row][col]