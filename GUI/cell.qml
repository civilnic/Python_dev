import QtQuick 2.4
import QtQuick.Controls 1.3
import QtQuick.Layouts 1.1
ApplicationWindow {
    title: qsTr("Fenêtre de connexion")
    width: 400
    height: 200
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
        Label { text: "QML est vraiment merveilleux" }
    }
    GridLayout {
        id: grid
        anchors.fill: parent // Ancre la disposition au composant souhaité
        columns: 2           // Nombre de colonnes
        anchors.margins: 5   // Marge entre la disposition et les bords de son conteneur
        columnSpacing: 10    // Espace entre chaque colonne
        Label {
            text: "Identifiant"
        }
        TextField {
            id: login
            Layout.fillWidth: true
            placeholderText: qsTr("Enter your login")
        }
        Label {
            text: "Mot de passe"
        }
        TextField {
            id: password
            Layout.fillWidth: true
            placeholderText: qsTr("Enter your password")
            echoMode: TextInput.Password
        }
        Button {
            text: "Se connecter"
            // Ces deux lignes autorisent le redimensionnement automatique du composant
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.columnSpan: 2    // Étalé sur deux colonnes
        }
        Label {
            id: result
            text : "Non connecté"
            Layout.fillWidth: true
            Layout.columnSpan: grid.columns // Étalé sur toutes les colonnes
        }
    }
}
