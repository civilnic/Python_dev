import QtQuick 2.0
import CustomModel 1.0

MEX_INTG_GUI {
    width: 450
    height: 400
    visible: true
    title: "MEX_INTG_GUI"

    MyModel: CustomModel {
        file: "choice_cnx.csv"

    }
}
