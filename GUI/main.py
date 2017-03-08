import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load('cell.qml')
    win = engine.rootObjects()[0]
    win.show()
    sys.exit(app.exec_())
