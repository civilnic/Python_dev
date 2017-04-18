import QtQuick 2.7
import QtQuick.Controls 1.5
import QtQuick.Dialogs 1.2

import CustomModel 1.0

ApplicationWindow {
    title: qsTr("CNX MERGE HMI")
    width: 2100
    height: 1000

    property var fileCsv

    MyModel: CustomModel {
        file: fileCsv
    }

    TableView {
        id: csvTab
        anchors.fill: parent

        model: MyModel
        onRowCountChanged: {
           selection.clear();
           selection.select(rowCount - 1);
}

        TableViewColumn {
            role: "Key"
            title: "Key"
            width: 130
        }

        TableViewColumn {
            role: "Priority"
            title: "Priority"
            width: 130
        }

    }


    menuBar: MenuBar {
        Menu {
            title: qsTr("&File")
            MenuItem {
                text : "Une action"
                onTriggered: console.log("Magique cette barre de menu")
            }
        }
    }
    statusBar: StatusBar {
        Label { text: "QML test" }
    }

}
