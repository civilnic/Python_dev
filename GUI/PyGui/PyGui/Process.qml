import QtQuick 2.7
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.0
import "content"

Item {
    ListModel {
        id: pageModel
        ListElement {
            title: "Signal names process"
            page: "content/ButtonPage.qml"
        }
        ListElement {
            title: "Compare/import connections process"
            page: "content/SliderPage.qml"
        }
        ListElement {
            title: "Compare/import intializations process"
            page: "content/ProgressBarPage.qml"
        }
        ListElement {
            title: "Flow comparison"
            page: "content/TabBarPage.qml"
        }

    }

    StackView {
        id: stackView
        anchors.fill: parent
        // Implements back key navigation
        focus: true
        Keys.onReleased: if (event.key === Qt.Key_Back && stackView.depth > 1) {
                             stackView.pop();
                             event.accepted = true;
                         }

        initialItem: Item {
            width: parent.width
            height: parent.height
            ListView {
                model: pageModel
                anchors.fill: parent
                delegate: AndroidDelegate {
                    text: title
                    onClicked: stackView.push(Qt.resolvedUrl(page))
                }
            }
        }
    }
}
