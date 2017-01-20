import QtQuick 2.0
import QtQuick.Window 2.0

Item {
    width:Screen.width/2
    height: Screen.height/10

    Rectangle{
        id:baseRec
        color: c
        width:Screen.width/2
        height: Screen.height/10


        Image{
            source: s
            width: height
            height: Screen.height/10
            anchors{
                verticalCenter: parent.verticalCenter
                leftMargin: 10
            }
        }
        Text{
            text:name
            anchors.centerIn: baseRec
            font.pixelSize: 22
        }
        Text{
            text: p
            font.pixelSize: 22
            anchors{
                verticalCenter: parent.verticalCenter
                right:parent.right
            }
        }
    }

}
