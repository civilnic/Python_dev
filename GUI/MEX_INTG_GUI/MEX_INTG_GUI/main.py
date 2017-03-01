# import sys
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtQml import QQmlApplicationEngine
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#     engine.load('MEX_INTG_GUI.qml')
#     win = engine.rootObjects()[0]
#     win.show()
#     sys.exit(app.exec_())

from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTableView
from PyQt5.QtQml import QQmlApplicationEngine
import sys


class PaletteListModel(QtCore.QAbstractListModel):
    def __init__(self, colors=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__colors = colors

    def headerData(self, section, orientation, role):

        if role == QtCore.Qt.DisplayRole:

            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Palette")
            else:
                return QtCore.QString("Color %1").arg(section)

    def rowCount(self, parent):
        return len(self.__colors)

    def data(self, index, role):

        if role == QtCore.Qt.EditRole:
            return self.__colors[index.row()].name()

        if role == QtCore.Qt.ToolTipRole:
            return "Hex code: " + self.__colors[index.row()].name()

        if role == QtCore.Qt.DecorationRole:
            row = index.row()
            value = self.__colors[row]

            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)

            return icon

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__colors[row]

            return value.name()

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:

            row = index.row()
            color = QtGui.QColor(value)

            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index)
                return True
        return False

    # =====================================================#
    # INSERTING & REMOVING
    # =====================================================#
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))

        self.endInsertRows()

        return True

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)

        self.endRemoveRows()
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("plastique")

    # ALL OF OUR VIEWS
    listView = QListView()
    listView.show()

    treeView = QTreeView()
    treeView.show()
    #
    comboBox = QComboBox()
    comboBox.show()
    #
    #tableView = QTableView()
    #tableView.show()

    red = QtGui.QColor(255, 0, 0)
    green = QtGui.QColor(0, 255, 0)
    blue = QtGui.QColor(0, 0, 255)

    rowCount = 4
    columnCount = 6

    model = PaletteListModel([red, green, blue])
    model.insertRows(0, 5)

    listView.setModel(model)
    comboBox.setModel(model)
    #tableView.setModel(model)
    treeView.setModel(model)

    sys.exit(app.exec_())