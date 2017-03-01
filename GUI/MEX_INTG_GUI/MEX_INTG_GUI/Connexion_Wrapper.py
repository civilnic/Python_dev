from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class ConnexionWrapper(QObject):

    def __init__(self, thing):
        QtCore.QObject.__init__(self)
        self._thing = thing


    def _name(self):
        return str(self._thing)


    changed = QtCore.Signal()

    name = QtCore.Property(unicode,_name, notify=changed)
