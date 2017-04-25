import QtQuick 2.7
import TestModel 1.0

Mex {
    width: 450
    height: 400
    visible: true
    title: "MEX_INTG_GUI"

    MyModel: TestModel {
        file: "choice_cnx.csv"
    }
}
