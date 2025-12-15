# -*- coding: utf-8 -*-
import dashboard_kasir_main as dkm
import session as s
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from kendaraan import Kendaraan, Kendaraan_pribadi, Bus


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(90, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        
        self.label_nopol = QtWidgets.QLabel(self.centralwidget)
        self.label_nopol.setGeometry(QtCore.QRect(20, 55, 100, 20))
        self.label_nopol.setObjectName("label_nopol")
        
        self.lineEdit_nopol = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_nopol.setGeometry(QtCore.QRect(130, 55, 320, 22))
        self.lineEdit_nopol.setObjectName("lineEdit_nopol")
        
        self.label_kategori = QtWidgets.QLabel(self.centralwidget)
        self.label_kategori.setGeometry(QtCore.QRect(20, 90, 100, 20))
        self.label_kategori.setObjectName("label_kategori")
        
        self.comboBox_kategori = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_kategori.setGeometry(QtCore.QRect(130, 90, 320, 22))
        self.comboBox_kategori.addItems(["Kendaraan Pribadi", "Bus"])
        self.comboBox_kategori.setObjectName("comboBox_kategori")
        
        self.label_jenis = QtWidgets.QLabel(self.centralwidget)
        self.label_jenis.setGeometry(QtCore.QRect(20, 125, 100, 20))
        self.label_jenis.setObjectName("label_jenis")
        
        self.comboBox_jenis = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_jenis.setGeometry(QtCore.QRect(130, 125, 320, 22))
        self.comboBox_jenis.addItems(["Motor", "Mobil"])
        self.comboBox_jenis.setObjectName("comboBox_jenis")
        
        self.label_kapasitas = QtWidgets.QLabel(self.centralwidget)
        self.label_kapasitas.setGeometry(QtCore.QRect(20, 160, 100, 20))
        self.label_kapasitas.setObjectName("label_kapasitas")
        
        self.spinBox_kapasitas = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_kapasitas.setGeometry(QtCore.QRect(130, 160, 320, 22))
        self.spinBox_kapasitas.setMinimum(0)
        self.spinBox_kapasitas.setMaximum(50)
        self.spinBox_kapasitas.setObjectName("spinBox_kapasitas")
        
        self.label_tarif = QtWidgets.QLabel(self.centralwidget)
        self.label_tarif.setGeometry(QtCore.QRect(20, 195, 100, 20))
        self.label_tarif.setObjectName("label_tarif")
        
        self.lineEdit_tarif = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_tarif.setGeometry(QtCore.QRect(130, 195, 320, 22))
        self.lineEdit_tarif.setReadOnly(True)
        self.lineEdit_tarif.setObjectName("lineEdit_tarif")
        
        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(20, 230, 430, 120))
        self.label_info.setObjectName("label_info")
        self.label_info.setWordWrap(True)
        
        self.pushButton_simpan = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_simpan.setGeometry(QtCore.QRect(160, 360, 90, 28))
        self.pushButton_simpan.setObjectName("pushButton_simpan")
        
        self.pushButton_batal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_batal.setGeometry(QtCore.QRect(270, 360, 90, 28))
        self.pushButton_batal.setObjectName("pushButton_batal")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.comboBox_kategori.currentIndexChanged.connect(self.on_kategori_changed)
        self.comboBox_jenis.currentIndexChanged.connect(self.on_jenis_changed)
        self.spinBox_kapasitas.valueChanged.connect(self.on_kapasitas_changed)
        self.pushButton_simpan.clicked.connect(self.simpan_masuk)
        self.pushButton_batal.clicked.connect(self.batal)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kendaraan Masuk"))
        self.label_title.setText(_translate("MainWindow", "Kendaraan Masuk"))
        self.label_nopol.setText(_translate("MainWindow", "No. Polisi:"))
        self.label_kategori.setText(_translate("MainWindow", "Jenis Kendaraan:"))
        self.label_jenis.setText(_translate("MainWindow", "Jenis:"))
        self.label_kapasitas.setText(_translate("MainWindow", "Kapasitas:"))
        self.label_tarif.setText(_translate("MainWindow", "Tarif/Jam:"))
        self.pushButton_simpan.setText(_translate("MainWindow", "Simpan"))
        self.pushButton_batal.setText(_translate("MainWindow", "Batal"))
        self.on_kategori_changed()

    def on_kategori_changed(self):
        kategori = self.comboBox_kategori.currentText()
        if kategori == "Kendaraan Pribadi":
            self.comboBox_jenis.clear()
            self.comboBox_jenis.addItems(["Motor", "Mobil"])
            self.spinBox_kapasitas.setVisible(False)
            self.label_kapasitas.setVisible(False)
            self.update_info_pribadi()
            self.update_tarif_pribadi()
        else:  # Bus
            self.comboBox_jenis.clear()
            self.comboBox_jenis.addItems(["Elf", "Bus"])
            self.spinBox_kapasitas.setVisible(True)
            self.label_kapasitas.setVisible(True)
            self.spinBox_kapasitas.setValue(0)
            self.update_info_bus()
            self.on_kapasitas_changed()

    def on_jenis_changed(self):
        kategori = self.comboBox_kategori.currentText()
        if kategori == "Kendaraan Pribadi":
            self.update_tarif_pribadi()
        else:
            self.on_kapasitas_changed()

    def on_kapasitas_changed(self):
        kategori = self.comboBox_kategori.currentText()
        if kategori == "Bus":
            kapasitas = self.spinBox_kapasitas.value()
            jenis = self.comboBox_jenis.currentText()
            
            if jenis == "Elf":
                if kapasitas < 8:
                    self.spinBox_kapasitas.setValue(8)
                    kapasitas = 8
                elif kapasitas > 15:
                    self.spinBox_kapasitas.setValue(15)
                    kapasitas = 15
            else:  # Bus
                if kapasitas < 12:
                    self.spinBox_kapasitas.setValue(12)
                    kapasitas = 12
                elif kapasitas > 40:
                    self.spinBox_kapasitas.setValue(40)
                    kapasitas = 40
            
            tarif = Kendaraan.hitung_tarif_bus(kapasitas)
            self.lineEdit_tarif.setText(f"Rp {tarif:,}")
            self.update_info_bus()

    def update_tarif_pribadi(self):
        jenis = self.comboBox_jenis.currentText()
        if jenis == "Motor":
            tarif = 2500
        else:  # Mobil
            tarif = 5000
        self.lineEdit_tarif.setText(f"Rp {tarif:,}")

    def update_info_pribadi(self):
        info = "Kendaraan Pribadi:\n"
        info += "- Motor: Rp 2.500/jam\n"
        info += "- Mobil: Rp 5.000/jam"
        self.label_info.setText(info)

    def update_info_bus(self):
        jenis = self.comboBox_jenis.currentText()
        if jenis == "Elf":
            info = "Bus Elf:\n"
            info += "- Kapasitas: 8 - 15 orang\n"
            info += "- Tarif: Rp 10.000 + Rp 2.500/5 penumpang extra"
        else:
            info = "Bus:\n"
            info += "- Kapasitas: 12 - 40 orang\n"
            info += "- Tarif: Rp 10.000 + Rp 2.500/5 penumpang extra"
        self.label_info.setText(info)

    def simpan_masuk(self):
        try:
            nopol = self.lineEdit_nopol.text().strip().upper()
            kategori = self.comboBox_kategori.currentText()
            jenis = self.comboBox_jenis.currentText()
            petugas = s.current_user
            
            if not nopol:
                QMessageBox.warning(None, "Error", "No. Polisi tidak boleh kosong!")
                return
            
            if Kendaraan.is_nopol_exists(nopol):
                QMessageBox.warning(None, "Error", f"Nopol {nopol} sudah terparkir!")
                return
            
            if kategori == "Kendaraan Pribadi":
                tarif = 2500 if jenis == "Motor" else 5000
                obj = Kendaraan_pribadi()
                obj.kendaraan_masuk(nopol, jenis, tarif, petugas)
            else:  # Bus
                kapasitas = self.spinBox_kapasitas.value()
                tarif = Kendaraan.hitung_tarif_bus(kapasitas)
                obj = Bus()
                obj.kendaraan_masuk(nopol, jenis, kapasitas, tarif, petugas)
            
            QMessageBox.information(None, "Sukses", f"Kendaraan {nopol} berhasil dicatat masuk.")
            self.batal()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Terjadi error: {e}")

    def batal(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = dkm.Ui_MainWindow()
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
