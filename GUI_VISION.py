# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_VISION.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(70, 40, 661, 431))
        self.groupBox.setObjectName("groupBox")
        self.Inciar_video = QtWidgets.QPushButton(self.groupBox)
        self.Inciar_video.setGeometry(QtCore.QRect(10, 290, 75, 23))
        self.Inciar_video.setObjectName("Inciar_video")
        self.Stop_video = QtWidgets.QPushButton(self.groupBox)
        self.Stop_video.setGeometry(QtCore.QRect(130, 290, 75, 23))
        self.Stop_video.setObjectName("Stop_video")
        self.Bordes = QtWidgets.QPushButton(self.groupBox)
        self.Bordes.setGeometry(QtCore.QRect(324, 290, 91, 21))
        self.Bordes.setObjectName("Bordes")
        self.Binario = QtWidgets.QPushButton(self.groupBox)
        self.Binario.setGeometry(QtCore.QRect(430, 290, 75, 23))
        self.Binario.setObjectName("Binario")
        self.Grises = QtWidgets.QPushButton(self.groupBox)
        self.Grises.setGeometry(QtCore.QRect(520, 290, 91, 21))
        self.Grises.setObjectName("Grises")
        self.CanalRojo = QtWidgets.QPushButton(self.groupBox)
        self.CanalRojo.setGeometry(QtCore.QRect(340, 340, 75, 23))
        self.CanalRojo.setObjectName("CanalRojo")
        self.CanalAzul = QtWidgets.QPushButton(self.groupBox)
        self.CanalAzul.setGeometry(QtCore.QRect(440, 340, 75, 23))
        self.CanalAzul.setObjectName("CanalAzul")
        self.CanalVerde = QtWidgets.QPushButton(self.groupBox)
        self.CanalVerde.setGeometry(QtCore.QRect(540, 340, 75, 23))
        self.CanalVerde.setObjectName("CanalVerde")
        self.Gaussiano = QtWidgets.QPushButton(self.groupBox)
        self.Gaussiano.setGeometry(QtCore.QRect(440, 380, 75, 23))
        self.Gaussiano.setObjectName("Gaussiano")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 60, 191, 181))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(330, 50, 281, 211))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.Inciar_video.setText(_translate("MainWindow", "Start video"))
        self.Stop_video.setText(_translate("MainWindow", "Stop Video"))
        self.Bordes.setText(_translate("MainWindow", "Detectar bordes"))
        self.Binario.setText(_translate("MainWindow", "Binarizar"))
        self.Grises.setText(_translate("MainWindow", "Escala de grises"))
        self.CanalRojo.setText(_translate("MainWindow", "Canal rojo"))
        self.CanalAzul.setText(_translate("MainWindow", "Canal azul "))
        self.CanalVerde.setText(_translate("MainWindow", "Canal verde"))
        self.Gaussiano.setText(_translate("MainWindow", "Gaussiano"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
