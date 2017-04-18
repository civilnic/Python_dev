import sys
import csv
from GUI.MEX_INTG_GUI.MEX_INTG_GUI.Connexion_Wrapper import CustomModel

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from PyQt5.QtQml import qmlRegisterType

# Main Function
if __name__ == '__main__':

    _file = r"choice_cnx.csv"
    _qml = r'main.qml'

    _data = []
    _csvFile = open(_file, 'r')
    _reader = csv.reader(_csvFile, delimiter=';')
    for _line in _reader:
       _data.append(_line)
    print(_data)

    app = QApplication(sys.argv)
    qmlRegisterType(CustomModel, 'CustomModel', 1, 0, 'CustomModel')
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    engine.load(_qml)

    win = engine.rootObjects()[0]
    win.show()
    sys.exit(app.exec_())


