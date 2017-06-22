import QtQuick 2.7

Test {
    property var fromPython

    width: 450
    height: 400
    visible: true
    title: "MEX_INTG_GUI"

    MyVar: fromPython
}
