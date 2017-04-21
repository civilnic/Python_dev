import os
import csv
from PyQt5.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QAbstractListModel, QModelIndex, Qt,QAbstractItemModel



class TestModel(QAbstractListModel):

    def __init__(self):

        QAbstractListModel.__init__(self)

        self._data = None
        self._roles = {}
        self._file = None
        self._just_created = False













class CustomModel(QAbstractListModel):

    def __init__(self, data, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)

        self._data = data
        self._roles = {}
        self._file = None
        self._just_created = False

    def _file_read(self):
        if self._file is None:
            return False

        with open(self._file, 'r') as _csvFile:

            _reader = csv.reader(_csvFile, delimiter=';')
            _csv = []

            for _line in _reader:
                _csv.append(_line)

            self._data = _csv[1:]

            for k in _csv[0]:
                self._roles[_csv[0].index(k)] = _csv[0][_csv[0].index(k)].encode('utf-8')
            #self._roles = {_csv[0].index(k): _csv[0][_csv[0].index(k)].encode('utf-8') for k in _csv[0]}

        return True

    def rowCount(self, parent=QModelIndex()):
        if self._file is None:
            return 0
        return len(self._data)

    def data(self, index, role):
        if self._file is None or not index.isValid():
            return None

        return self._data[index.row()][self._roles[role].decode('utf-8')]

    def setData(self, index, value, role):
        if self._file is None or not index.isValid():
            return False
        self._data[index.row()] = value

        if self._roles is None:
            self._roles = dict(zip(range(Qt.UserRole + 1, Qt.UserRole + 1 + len(value)),
                                   [v.encode('utf-8') for v in value.keys()]))

        self.dataChanged.emit(index, index, self._roles.keys())
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
        super(QAbstractListModel, self).endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def roleNames(self):
        return self._roles

    countChanged = pyqtSignal()

    @pyqtProperty(int, notify=countChanged)
    def count(self):
        return self.rowCount()

    @pyqtSlot(int, str, result=bool)
    def insert(self, row, value):
        index = self.createIndex(row, 0)
        return self.insertRows(row, 1) and self.setData(index, value, Qt.EditRole)

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
        return True

    @pyqtSlot(int, str, result=str)
    def get(self, index, role_name):
        if self._file is None:
            return None
        return self._data[index.row()][self._data[0].index(role_name)]

    @pyqtProperty(bool)
    def justCreated(self):
        return self._just_created


    @pyqtProperty(str)
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

        if os.path.isfile(self._file) and os.path.getsize(self._file) > 0:
            self._file_read()
        else:
            self._just_created = True
            self._data = []