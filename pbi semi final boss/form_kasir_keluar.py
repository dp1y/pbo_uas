# -*- coding: utf-8 -*-

import dashboard_kasir_main as dkm
import session as s
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from datetime import datetime
from kendaraan import Kendaraan, Kendaraan_pribadi, Bus




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(130, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        
        self.label_nopol = QtWidgets.QLabel(self.centralwidget)
        self.label_nopol.setGeometry(QtCore.QRect(20, 55, 100, 20))
        self.label_nopol.setObjectName("label_nopol")
        
        self.lineEdit_nopol = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_nopol.setGeometry(QtCore.QRect(130, 55, 380, 22))
        self.lineEdit_nopol.setObjectName("lineEdit_nopol")
        
        self.pushButton_cari = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cari.setGeometry(QtCore.QRect(515, 54, 70, 24))
        self.pushButton_cari.setObjectName("pushButton_cari")
        
        self.tableWidget_detail = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_detail.setGeometry(QtCore.QRect(20, 90, 560, 200))
        self.tableWidget_detail.setObjectName("tableWidget_detail")
        self.tableWidget_detail.setColumnCount(2)
        self.tableWidget_detail.setHorizontalHeaderLabels(["Info", "Detail"])
        
        self.label_subtotal = QtWidgets.QLabel(self.centralwidget)
        self.label_subtotal.setGeometry(QtCore.QRect(20, 300, 560, 60))
        self.label_subtotal.setObjectName("label_subtotal")
        self.label_subtotal.setWordWrap(True)
        
        self.pushButton_keluar = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_keluar.setGeometry(QtCore.QRect(180, 370, 90, 28))
        self.pushButton_keluar.setObjectName("pushButton_keluar")
        
        self.pushButton_batal = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_batal.setGeometry(QtCore.QRect(330, 370, 90, 28))
        self.pushButton_batal.setObjectName("pushButton_batal")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.pushButton_cari.clicked.connect(self.cari_kendaraan)
        self.pushButton_keluar.clicked.connect(self.keluar_kendaraan)
        self.pushButton_batal.clicked.connect(self.batal)

        self.current_kendaraan = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kendaraan Keluar"))
        self.label_title.setText(_translate("MainWindow", "Kendaraan Keluar"))
        self.label_nopol.setText(_translate("MainWindow", "No. Polisi:"))
        self.pushButton_cari.setText(_translate("MainWindow", "Cari"))
        self.label_subtotal.setText(_translate("MainWindow", "Subtotal Tarif: -"))
        self.pushButton_keluar.setText(_translate("MainWindow", "Keluar"))
        self.pushButton_batal.setText(_translate("MainWindow", "Batal"))

    def cari_kendaraan(self):
        try:
            nopol = self.lineEdit_nopol.text().strip().upper()
            if not nopol:
                QMessageBox.warning(None, "Error", "Masukkan No. Polisi terlebih dahulu!")
                return
            detail = Kendaraan.get_kendaraan_detail(nopol)
            if not detail:
                QMessageBox.warning(None, "Error", f"Kendaraan dengan nopol {nopol} tidak ditemukan!")
                self.tableWidget_detail.setRowCount(0)
                self.label_subtotal.setText("Subtotal Tarif: -")
                return

            self.current_kendaraan = detail
            self.tampil_detail(detail)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Terjadi error: {e}")

    def tampil_detail(self, detail):
        try:
            nopol, waktu_masuk, waktu_keluar, status = detail
            
            self.tableWidget_detail.setRowCount(0)
            
            rows = [
                ["No. Polisi", nopol],
                ["Waktu Masuk", str(waktu_masuk)],
                ["Status", status],
            ]
            
            info_pribadi = self.get_detail_pribadi(nopol)
            info_bus = self.get_detail_bus(nopol)
            
            jenis = "Tidak diketahui"
            tarif_per_jam = 0
            
            if info_pribadi:
                jenis, tarif_per_jam = info_pribadi
                rows.append(["Jenis", jenis])
                rows.append(["Tarif/Jam", f"Rp {tarif_per_jam:,}"])
            elif info_bus:
                jenis, kapasitas, tarif_per_jam = info_bus
                rows.append(["Jenis Bus", jenis])
                rows.append(["Kapasitas", str(kapasitas)])
                rows.append(["Tarif/Jam", f"Rp {tarif_per_jam:,}"])
            
            for i, row in enumerate(rows):
                self.tableWidget_detail.insertRow(i)
                self.tableWidget_detail.setItem(i, 0, QTableWidgetItem(row[0]))
                self.tableWidget_detail.setItem(i, 1, QTableWidgetItem(row[1]))
            
            waktu_keluar_now = datetime.now()
            subtotal, jam = Kendaraan.hitung_tarif(waktu_masuk, waktu_keluar_now, tarif_per_jam)
            self.label_subtotal.setText(f"Durasi: {jam:.1f} jam\nSubtotal Tarif: Rp {subtotal:,}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Terjadi error saat menampilkan detail: {e}")

    def get_detail_pribadi(self, nopol):
        try:
            return Kendaraan.get_detail_pribadi(nopol)
        except Exception as e:
            print(f"Error get_detail_pribadi: {e}")
            return None

    def get_detail_bus(self, nopol):
        try:
            return Kendaraan.get_detail_bus(nopol)
        except Exception as e:
            print(f"Error get_detail_bus: {e}")
            return None

    def keluar_kendaraan(self):
        if not self.current_kendaraan:
            QMessageBox.warning(None, "Error", "Cari kendaraan terlebih dahulu!")
            return
        
        nopol = self.current_kendaraan[0]
        try:
            petugas = s.current_user
            obj = Kendaraan()
            obj.status = "keluar"
            obj.kendaraan_keluar(nopol,petugas)
            QMessageBox.information(None, "Sukses", f"Kendaraan {nopol} berhasil keluar.")
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
