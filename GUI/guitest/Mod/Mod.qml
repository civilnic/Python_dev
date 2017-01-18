import QtQuick 2.7
import QtQuick.Window 2.2

Rectangle
{
    width:Screen.width/2
    height: Screen.height/2

    ListView{
        width:Screen.width/2
        height: Screen.height/2
        spacing: 10
        header: Header{}
        model:mod

        delegate:MyDel{}

    }

    MyModel{id:mod}
}
