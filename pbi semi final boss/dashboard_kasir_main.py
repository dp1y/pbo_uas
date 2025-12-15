# -*- coding: utf-8 -*-

import form_kasir_masuk as fkm
import form_kasir_keluar as fkk
import view_parkiran as vp
import form_login as fl
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(220, 60, 361, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_masuk = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_masuk.setGeometry(QtCore.QRect(140, 140, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_masuk.setFont(font)
        self.pushButton_masuk.setObjectName("pushButton_masuk")
        self.pushButton_keluar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_keluar.setGeometry(QtCore.QRect(470, 140, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_keluar.setFont(font)
        self.pushButton_keluar.setObjectName("pushButton_keluar")
        self.pushButton_lihat = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_lihat.setGeometry(QtCore.QRect(140, 270, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_lihat.setFont(font)
        self.pushButton_lihat.setObjectName("pushButton_lihat")
        self.pushButton_logout = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_logout.setGeometry(QtCore.QRect(470, 270, 191, 101))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_logout.setFont(font)
        self.pushButton_logout.setObjectName("pushButton_logout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton_masuk.clicked.connect(self.openFormMasuk)
        self.pushButton_keluar.clicked.connect(self.openFormKeluar)
        self.pushButton_lihat.clicked.connect(self.openViewParkiran)
        self.pushButton_logout.clicked.connect(self.logout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Petugas Parkir"))
        self.label.setText(_translate("MainWindow", "PETUGAS PARKIR"))
        self.pushButton_masuk.setText(_translate("MainWindow", "Kendaraan Masuk"))
        self.pushButton_keluar.setText(_translate("MainWindow", "Kendaraan Keluar"))
        self.pushButton_lihat.setText(_translate("MainWindow", "Kondisi Parkiran"))
        self.pushButton_logout.setText(_translate("MainWindow", "Log Out"))

    def openFormMasuk(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = fkm.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.centralwidget.window().close()

    def openFormKeluar(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = fkk.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.centralwidget.window().close()

    def openViewParkiran(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = vp.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.centralwidget.window().close()

    def logout(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = fl.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        self.centralwidget.window().close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
