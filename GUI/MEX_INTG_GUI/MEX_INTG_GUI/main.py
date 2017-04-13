import sys
import csv
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QUrl, QVariant
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from GUI.MEX_INTG_GUI.MEX_INTG_GUI.Connexion_Wrapper import ConnexionWrapper

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine

# Main Function
if __name__ == '__main__':

   _file = r"choice_cnx.csv"
   _qml = r'MEX_INTG_GUI\MEX_INTG_GUI.qml'
   #_Cnx_Wrapp = ConnexionWrapper()
   #print(_Cnx_Wrapp.rowCountlt())
   #print(_Cnx_Wrapp.columnCountlt())
   #print(_Cnx_Wrapp.datalt(0, 10))

   # app = QGuiApplication(sys.argv)
   # view = QQuickView()
   #
   # ctxt = view.rootContext()
   # ctxt.setContextProperty('ConnexionWrapper', _Cnx_Wrapp)
   # view.setResizeMode(QQuickView.SizeRootObjectToView)
   # view.setSource(QUrl.fromLocalFile(_qml))
   # view.show()
   #
   # sys.exit(app.exec_())

   _csvFile = open(_file, "r")
   _reader = csv.reader(_csvFile, delimiter=';')

   app = QApplication(sys.argv)
   qmlRegisterType(ConnexionWrapper, 'cnxWrapper', 1, 0, 'ConnexionWrapper')
   engine = QQmlApplicationEngine()
   engine.quit.connect(app.quit)
   engine.rootContext().setContextProperty("csv_file", _reader)
   engine.load(_qml)
   sys.exit(app.exec_())


