from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import csv
import sys
import os
import json
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QAbstractListModel, QModelIndex, Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlListProperty

class ConnexionWrapper__(QAbstractTableModel):



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


class ConnexionWrapper(QAbstractListModel):

    def __init__(self, data, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)

        self._objectTab = []
        self._filename = r"choice_cnx.csv"

        self._data = data
        self._file = None
        self._just_created = False

    def _file_write(self):
        if self._file is None:
            return False

        with open(self._file, 'w') as f:
            json.dump(self._data, f)
        return True

    def rowCount(self, parent=QModelIndex()):
        if self._file is None:
            return 0
        return len(self._data)

    def data(self, index, role):
        if self._file is None or not index.isValid():
            return None
        return self._data[index.row()]

    def setData(self, index, value, role):
        if self._file is None or not index.isValid():
            return False

        self._data[index.row()] = value
        self.dataChanged.emit(index, index, [role])
        self._file_write()
        return True

    def insertRows(self, row, count, parent=None):
        if self._file is None:
            return False

        super(QAbstractListModel, self).beginInsertRows(QModelIndex(), row, row + count - 1)
        for i in range(count):
            self._data.insert(row + i, None)
        super(QAbstractListModel, self).endInsertRows()
        self.countChanged.emit()
        return True

    def removeRows(self, row, count, parent=None):
        if self._file is None:
            return False

        super(QAbstractListModel, self).beginRemoveRows(QModelIndex(), row, row + count - 1)
        for i in range(count):
            del self._data[row]
        self._file_write()
        super(QAbstractListModel, self).endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def roleNames(self):
        return {Qt.UserRole + 1: b"text"}

    countChanged = pyqtSignal()

    @pyqtProperty(int, notify=countChanged)
    def count(self):
        return self.rowCount()

    @pyqtSlot(int, str, result=bool)
    def insert(self, row, value):
        return self.insertRows(row, 1) and self.setData(self.createIndex(row, 0), value, Qt.EditRole)

    @pyqtSlot(str, result=bool)
    def append(self, value):
        return self.insert(self.count, value)

    @pyqtSlot(int, result=bool)
    def remove(self, index):
        if self._file is None:
            return False

        super(QAbstractListModel, self).beginRemoveRows(QModelIndex(), index, index)
        del self._data[index]
        super(QAbstractListModel, self).endRemoveRows()
        self._file_write()
        return True

    @pyqtSlot(int, result=str)
    def get(self, index):
        if self._file is None:
            return None
        return self._data[index]

    @pyqtProperty(str)
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value
        if os.path.isfile(self._file) and os.path.getsize(self._file) > 0:
            with open(self._file, 'r') as f:
                self._data = json.load(f)
        else:
            self._just_created = True
            self._data = []

    @pyqtProperty(bool)
    def justCreated(self):
        return self._just_created

    @pyqtSlot(str, result=int)
    def findIndexByName(self, value):
        return [i for i in range(len(self._data)) if self._data[i] == value][0]