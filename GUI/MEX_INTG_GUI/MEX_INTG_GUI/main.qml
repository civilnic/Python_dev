import QtQuick 2.0
import TestModel 1.0

MEX_INTG_GUI {
    width: 450
    height: 400
    visible: true
    title: "MEX_INTG_GUI"

    MyModel: TestModel {
        file: "choice_cnx.csv"

    }
}
