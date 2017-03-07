from PyQt5.QtCore import QAbstractTableModel
from PyQt5 import QtCore
import csv

class ConnexionWrapper(QAbstractTableModel):

    def __init__(self, filename, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._thing = "cnw_wrapper"

        self._filename = filename

        _csvFile = open(self._filename, "r")

        self._linesList = csv.reader(_csvFile, delimiter=';')

    def _name(self):
        return str(self._thing)

    def rowCount(self, parent):
        return len(self._linesList)

    def columnCount(self, parent):
        return len(self._linesList[0])

