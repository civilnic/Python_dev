import sys
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

   _file = r"F:\Mes documents\Nicolas\Boulot\Developpement\Python\Python_dev\GUI\choice_cnx.csv"
   _qml = r'F:\Mes documents\Nicolas\Boulot\Developpement\Python\Python_dev\GUI\MEX_INTG_GUI\MEX_INTG_GUI\MEX_INTG_GUI.qml'
   _Cnx_Wrapp = ConnexionWrapper(_file)
   print(_Cnx_Wrapp.rowCountlt())
   print(_Cnx_Wrapp.columnCountlt())
   print(_Cnx_Wrapp.datalt(10,10))

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


   app = QApplication(sys.argv)
   qmlRegisterType(ConnexionWrapper, 'cnxWrapper', 1, 0, 'ConnexionWrapper')
   engine = QQmlApplicationEngine(parent=app)
   engine.load(_qml)
   win = engine.rootObjects()[0]
   win.show()
   sys.exit(app.exec_())

