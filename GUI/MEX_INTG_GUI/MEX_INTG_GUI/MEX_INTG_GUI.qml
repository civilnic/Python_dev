import QtQuick 2.7
import QtQuick.Controls 1.5
import QtQuick.Dialogs 1.2

import cnxWrapper 1.0

ApplicationWindow {
    title: qsTr("CNX MERGE HMI")
    width: 2100
    height: 1000

    Component {
        id: textDelegate
        Text {
            text: role
        }
    }

    TableView {
        model: ConnexionWrapper
        x: 0
        y: 0
        width: 2100
        height: 1000
        TableViewColumn{
            role: "Key"
            title: "Key"
        }

        TableViewColumn{
            role: "Flow Name"
            title: "Flow Name"
        }
        TableViewColumn{
            role: "Producer Model"
            title: "Producer Model"
        }
        TableViewColumn{
            role: "Producer port"
            title: "Producer port"
        }
        TableViewColumn{
            role: "Producer operator"
            title: "Producer operator"
        }
        TableViewColumn{
            role: "Signal Name"
            title: "Signal Name"
        }
        TableViewColumn{
            role: "Consumer Model"
            title: "Consumer Model"
        }
        TableViewColumn{
            role: "Consumer port"
            title: "Consumer port"
        }
        TableViewColumn{
            role: "Consumer Operator"
            title: "Consumer Operator"
        }
        TableViewColumn{
            role: "Priority"
            title: "Priority"
        }
        TableViewColumn{
            role: "Automatic Choice Available"
            title: "Automatic Choice Available"
        }
        TableViewColumn{
            role: "Manual Choice"
            title: "Manual Choice"
        }
        TableViewColumn{
            role: "Comment"
            title: "Comment"
        }
        itemDelegate: textDelegate

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
