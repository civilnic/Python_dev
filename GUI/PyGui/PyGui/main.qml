import QtQuick 2.2

import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.0



ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("CNX MERGE GUI")

    Item {
        width: 580
        height: 400
        SystemPalette { id: palette }
        clip: true

        FileDialog {
            id: fileDialog
            visible: fileDialogVisible.checked
            modality: fileDialogModal.checked ? Qt.WindowModal : Qt.NonModal
            title: fileDialogSelectFolder.checked ? "Choose a folder" :
                (fileDialogSelectMultiple.checked ? "Choose some files" : "Choose a file")
            selectExisting: fileDialogSelectExisting.checked
            selectMultiple: fileDialogSelectMultiple.checked
            selectFolder: fileDialogSelectFolder.checked
            nameFilters: [ "Image files (*.png *.jpg)", "All files (*)" ]
            selectedNameFilter: "All files (*)"
            sidebarVisible: fileDialogSidebarVisible.checked
            onAccepted: {
                console.log("Accepted: " + fileUrls)
                if (fileDialogOpenFiles.checked)
                    for (var i = 0; i < fileUrls.length; ++i)
                        Qt.openUrlExternally(fileUrls[i])
            }
            onRejected: { console.log("Rejected") }
        }

        ScrollView {
            id: scrollView
            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
                bottom: bottomBar.top
                leftMargin: 12
            }
            ColumnLayout {
                spacing: 8
                Item { Layout.preferredHeight: 4 } // padding
                Label {
                    font.bold: true
                    text: "Selected MEXICO data base flow file"
                }
                CheckBox {
                    id: fileDialogModal
                    text: "Modal"
                    checked: true
                    Binding on checked { value: fileDialog.modality != Qt.NonModal }
                }
                CheckBox {
                    id: fileDialogSelectFolder
                    text: "Select Folder"
                    Binding on checked { value: fileDialog.selectFolder }
                }
                CheckBox {
                    id: fileDialogSelectExisting
                    text: "Select Existing Files"
                    checked: true
                    Binding on checked { value: fileDialog.selectExisting }
                }
                CheckBox {
                    id: fileDialogSelectMultiple
                    text: "Select Multiple Files"
                    Binding on checked { value: fileDialog.selectMultiple }
                }
                CheckBox {
                    id: fileDialogOpenFiles
                    text: "Open Files After Accepting"
                }
                CheckBox {
                    id: fileDialogSidebarVisible
                    text: "Show Sidebar"
                    checked: fileDialog.sidebarVisible
                    Binding on checked { value: fileDialog.sidebarVisible }
                }
                CheckBox {
                    id: fileDialogVisible
                    text: "Visible"
                    Binding on checked { value: fileDialog.visible }
                }
                Label {
                    text: "<b>current view folder:</b> " + fileDialog.folder
                }
                Label {
                    text: "<b>name filters:</b> {" + fileDialog.nameFilters + "}"
                }
                Label {
                    text: "<b>current filter:</b>" + fileDialog.selectedNameFilter
                }
                Label {
                    text: "<b>chosen files:</b> " + fileDialog.fileUrls
                }
                Label {
                    text: "<b>chosen single path:</b> " + fileDialog.fileUrl
                }
            }
        }

        Rectangle {
            id: bottomBar
            anchors {
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }
            height: buttonRow.height * 1.2
            color: Qt.darker(palette.window, 1.1)
            border.color: Qt.darker(palette.window, 1.3)
            Row {
                id: buttonRow
                spacing: 6
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 12
                height: implicitHeight
                width: parent.width
                Button {
                    text: "Open"
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: fileDialog.open()
                }
                Button {
                    text: "Pictures"
                    tooltip: "go to my Pictures directory"
                    anchors.verticalCenter: parent.verticalCenter
                    enabled: fileDialog.shortcuts.hasOwnProperty("pictures")
                    onClicked: fileDialog.folder = fileDialog.shortcuts.pictures
                }
                Button {
                    text: "Home"
                    tooltip: "go to my home directory"
                    anchors.verticalCenter: parent.verticalCenter
                    enabled: fileDialog.shortcuts.hasOwnProperty("home")
                    onClicked: fileDialog.folder = fileDialog.shortcuts.home
                }
            }
        }

    }

}
