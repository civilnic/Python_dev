import sys
import csv
from GUI.MEX_INTG_GUI.MEX_INTG_GUI.Connexion_Wrapper import CustomModel,TestModel

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QUrl

from PyQt5.QtQml import qmlRegisterType

# Main Function
# if __name__ == '__main__':
#
#
#
#     _file = r"choice_cnx.csv"
#     _qml = r'main.qml'
#
#     _data = []
#     _csvFile = open(_file, 'r')
#     _reader = csv.reader(_csvFile, delimiter=';')
#     for _line in _reader:
#        _data.append(_line)
#
#     toto = {}
#     for k in _data[0]:
#         toto[_data[0].index(k)] = _data[0][_data[0].index(k)].encode('utf-8')
#     #toto = {int(k): _data[0][k].encode('utf-8') for k in _data[0]}
#     print(toto)
#
#     model = CustomModel()
#     model.file = _file
#     #print (model.get(1,"Key"))
#
#     app = QApplication(sys.argv)
#     qmlRegisterType(TestModel, 'TestModel', 1, 0, 'TestModel')
#     engine = QQmlApplicationEngine()
#     engine.setOutputWarningsToStandardError(True)
#
#     engine.quit.connect(app.quit)
#
#     engine.load(_qml)
#
#     win = engine.rootObjects()[0]
#     win.show()
#     sys.exit(app.exec_())

if __name__ == '__main__':

    _file = r"choice_cnx.csv"
    _qml = r'main.qml'

    # Prints QML errors
    def handleStatusChange(status):
        if status == QQuickView.Error:
            errors = view.errors()
            if errors:
                print (errors[0].description())

    myApp = QApplication(sys.argv)
    qmlRegisterType(TestModel, 'TestModel', 1, 0, 'TestModel')

    view = QQuickView()
    view.rootContext().setContextProperty('fromPython', "text de la nasa")
    view.statusChanged.connect(handleStatusChange)

    view.setSource(QUrl(_qml))

    try:
        sys.exit(myApp.exec_())
    except:
        print("Exiting")
