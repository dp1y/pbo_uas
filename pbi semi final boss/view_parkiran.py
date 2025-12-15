# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from kendaraan import Kendaraan
import dashboard_kasir_main as dkm


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(870, 580, 93, 28))
        self.pushButton_back.setObjectName("pushButton_back")
        
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(50, 130, 900, 380))
        self.tableView.setObjectName("tableView")
        
        self.lineEdit_cari = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_cari.setGeometry(QtCore.QRect(50, 90, 350, 31))
        self.lineEdit_cari.setObjectName("lineEdit_cari")
        
        self.comboBox_jenis = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_jenis.setGeometry(QtCore.QRect(420, 90, 150, 31))
        self.comboBox_jenis.setObjectName("comboBox_jenis")
        self.comboBox_jenis.addItems(["Semua", "Motor", "Mobil", "Elf", "Bus"])
        
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(300, 30, 400, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        
        self.pushButton_cari = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_cari.setGeometry(QtCore.QRect(580, 90, 80, 31))
        self.pushButton_cari.setObjectName("pushButton_cari")
        
        self.label_revenue = QtWidgets.QLabel(self.centralwidget)
        self.label_revenue.setGeometry(QtCore.QRect(700, 520, 250, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.label_revenue.setFont(font)
        self.label_revenue.setObjectName("label_revenue")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_back.clicked.connect(self.back)
        self.loadDataParkiran()
        self.pushButton_cari.clicked.connect(self.cariData)
        self.comboBox_jenis.currentIndexChanged.connect(self.cariData)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Kondisi Parkiran"))
        self.pushButton_back.setText(_translate("MainWindow", "Kembali"))
        self.label_title.setText(_translate("MainWindow", "Kondisi Parkiran"))
        self.pushButton_cari.setText(_translate("MainWindow", "Cari"))

    def loadDataParkiran(self):
        try:
            data = []
            try:
                data = Kendaraan.get_all_kendaraan_with_jenis()
            except Exception as e:
                print(f"Error loading data: {e}")
                data = []
            self.tampilDataTable(data)
            self.updateRevenue(data)
        except Exception as e:
            print(f"Error dalam loadDataParkiran: {e}")

    def tampilDataTable(self, data):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["No. Polisi", "Jenis Kendaraan", "Waktu Masuk", "Petugas Masuk", "Waktu Keluar", "Petugas Keluar", "Tarif/Jam"])
        
        for row in data:
            nopol, jenis, masuk, ptg_masuk, keluar, ptg_keluar, tarif, status = row
            items = [
                QStandardItem(str(nopol)),
                QStandardItem(str(jenis) if jenis else "-"),
                QStandardItem(str(masuk) if masuk else "-"),
                QStandardItem(str(ptg_masuk) if ptg_masuk else "-"),
                QStandardItem(str(keluar) if keluar else "-"),
                QStandardItem(str(ptg_keluar) if ptg_keluar else "-"),
                QStandardItem(f"Rp {int(tarif):,}".replace(",", ".") if tarif else "-")
            ]
            model.appendRow(items)
        
        self.tableView.setModel(model)
        
        for i in range(model.columnCount()):
            self.tableView.resizeColumnToContents(i)

    def updateRevenue(self, data):
        try:
            from datetime import date
            total = 0
            for row in data:
                nopol, jenis, masuk, ptg_masuk, keluar, ptg_keluar, tarif, status = row
                if masuk and masuk.date() == date.today() and status == 'keluar' and keluar:
                    durasi = keluar - masuk
                    jam = durasi.total_seconds() / 3600
                    if jam < 1:
                        jam = 1
                    total += int(jam * tarif)
            
            self.label_revenue.setText(f"Total Pendapatan: Rp {total:,}".replace(",", "."))
        except Exception as e:
            print(f"Error calculating revenue: {e}")
            self.label_revenue.setText("Total Pendapatan: Rp 0")

    def cariData(self):
        try:
            search_text = self.lineEdit_cari.text().strip()
            jenis_filter = self.comboBox_jenis.currentText()
            
            if not search_text and jenis_filter == "Semua":
                self.loadDataParkiran()
                return
            
            try:
                data = Kendaraan.search_kendaraan_with_jenis(search_text if search_text else "", jenis_filter if jenis_filter != "Semua" else None)
            except Exception as e:
                print(f"Error searching: {e}")
                data = []
            
            self.tampilDataTable(data)
            self.updateRevenue(data)
        except Exception as e:
            print(f"Error dalam cariData: {e}")

    def back(self):
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
