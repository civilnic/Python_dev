import QtQuick 2.7
import QtQuick.Controls 1.5
import QtQuick.Dialogs 1.2

ApplicationWindow
{
    id: window
    property var MyModel

    TableView {
        id: csvTab
        anchors.fill: parent

        model: MyModel

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
