# Raman Spectra 데이터 도식화 프로그램 구현

# Tab1
# 1개의 파일 불러오면 베이스라인 보정 전후 그래프 출력

# Tab2
# 2개의 파일 불러오면 베이스라인 보정 후 그래프 출력
# 그래프 마우스 오버 - 좌표 출력
# 그래프 Peak점 표시
# 2개의 파일의 x값 별 y값 차이값 데이터프레임 출력
# 데이터프레임 검색 - x좌표 검색 시 결과 출력

# Tab3
# Raman Peak Table 검색
# Pubmed 링크 버튼

# (+) 화면 반응형으로 수정


from PyQt5.QtGui import QDesktopServices
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from BaselineRemoval import BaselineRemoval
from scipy.signal import find_peaks, peak_prominences
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from PyQt5.QtCore import QUrl, QSize

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1327, 1246)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_1 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_1.setMaximumSize(QtCore.QSize(16777215, 70))
        self.groupBox_1.setTitle("")
        self.groupBox_1.setObjectName("groupBox_1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_1 = QtWidgets.QLabel(self.groupBox_1)
        self.label_1.setObjectName("label_1")
        self.gridLayout_4.addWidget(self.label_1, 0, 0, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.groupBox_1)
        self.pushButton_1.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_4.addWidget(self.pushButton_1, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 550))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 0, 1, 1)
        self.graphwidget_1 = PlotWidget(self.groupBox_2)
        self.graphwidget_1.setObjectName("graphwidget_1")
        self.gridLayout_5.addWidget(self.graphwidget_1, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_3.setMaximumSize(QtCore.QSize(16777215, 70))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_6.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_4.setMaximumSize(QtCore.QSize(16777215, 550))
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
        self.graphwidget_2 = PlotWidget(self.groupBox_4)
        self.graphwidget_2.setObjectName("graphwidget_2")
        self.gridLayout_7.addWidget(self.graphwidget_2, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_6.setMinimumSize(QtCore.QSize(450, 0))
        self.groupBox_6.setMaximumSize(QtCore.QSize(600, 16777215))
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.gridLayout_9.addWidget(self.lineEdit_1, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_9.addWidget(self.pushButton_5, 0, 1, 1, 1)
        self.tableView_1 = QtWidgets.QTableView(self.groupBox_6)
        self.tableView_1.setObjectName("tableView_1")
        self.gridLayout_9.addWidget(self.tableView_1, 1, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox_6)
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_7.setMinimumSize(QtCore.QSize(800, 0))
        self.groupBox_7.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_6 = QtWidgets.QLabel(self.groupBox_7)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_3.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_8.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.graphwidget_3 = PlotWidget(self.groupBox_7)
        self.graphwidget_3.setObjectName("graphwidget_3")
        self.gridLayout_8.addWidget(self.graphwidget_3, 1, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox_7)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_9)
        self.pushButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        self.label_7.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 1, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_9)
        self.pushButton_7.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_3.addWidget(self.pushButton_7, 0, 3, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_9, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_8)
        self.groupBox_11 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_11.setObjectName("groupBox_11")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_11)
        self.gridLayout.setObjectName("gridLayout")
        self.tableView_2 = QtWidgets.QTableView(self.groupBox_11)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_11)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_12 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_8 = QtWidgets.QLabel(self.groupBox_12)
        self.label_8.setObjectName("label_8")
        self.gridLayout_10.addWidget(self.label_8, 0, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_12)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_13 = QtWidgets.QGroupBox(self.tab_5)
        self.groupBox_13.setObjectName("groupBox_13")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_13)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_9 = QtWidgets.QLabel(self.groupBox_13)
        self.label_9.setObjectName("label_9")
        self.gridLayout_11.addWidget(self.label_9, 0, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.groupBox_13)
        self.tabWidget.addTab(self.tab_5, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Attach File"))
        self.pushButton_1.setText(_translate("MainWindow", "Attach File 1"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Graph 1"))
        self.label_2.setText(_translate("MainWindow", "Graph1"))
        self.label_3.setText(_translate("MainWindow", "Attact File"))
        self.pushButton_2.setText(_translate("MainWindow", "Attach File 2"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Graph 2"))
        self.label_4.setText(_translate("MainWindow", "Graph2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Baseline Correction"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Difference Value (File1 - File2)"))
        self.pushButton_5.setText(_translate("MainWindow", "Search"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Graph Comparsion"))
        self.label_6.setText(_translate("MainWindow", "Graph3"))
        self.pushButton_3.setText(_translate("MainWindow", "Attach 2 files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Comparsion"))
        self.groupBox_9.setTitle(_translate("MainWindow", "파수 구간 입력"))
        self.pushButton.setText(_translate("MainWindow", "PubMed"))
        self.label_7.setText(_translate("MainWindow", "~"))
        self.pushButton_7.setText(_translate("MainWindow", "Search"))
        self.groupBox_11.setTitle(_translate("MainWindow", "GroupBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Peak Table"))
        self.groupBox_12.setTitle(_translate("MainWindow", "GroupBox"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Help"))
        self.groupBox_13.setTitle(_translate("MainWindow", "GroupBox"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "About"))

        self.graphwidget_1.setBackground('w')
        self.graphwidget_2.setBackground('w')
        self.graphwidget_3.setBackground('w')

        self.pushButton.clicked.connect(self.open_pubmed_url)
        self.pushButton_1.clicked.connect(self.load_file_1)
        self.pushButton_2.clicked.connect(self.load_file_2)
        self.pushButton_3.clicked.connect(self.load_file_3)
        self.pushButton_5.clicked.connect(self.filter_data_by_wavelength)
        self.pushButton_7.clicked.connect(self.filter_raman_peaks)
        
        self.graphwidget_3.scene().sigMouseMoved.connect(self.updateTooltip)



    def open_pubmed_url(self):
        pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/"  # Replace this with the desired URL
        QDesktopServices.openUrl(QUrl(pubmed_url))

    def filter_data_by_wavelength(self):
        wavelength = int(self.lineEdit_1.text())

        filtered_df = self.df_change[self.df_change['Wavelength'] == wavelength]

        if self.tableView_1_model is not None:
            self.tableView_1_model.clear()

        model = PandasTableModel(filtered_df)
        self.tableView_1.setModel(model)

        self.tableView_1_model = model

        self.tableView_1.resizeColumnsToContents()

    def filter_raman_peaks(self):
        start_val = int(self.lineEdit_2.text())
        end_val = int(self.lineEdit_3.text())

        raman_peaks_data = {
            'Raman peaks (cm−1)':  [ 446,  494,  509,  523,  535,  545,  548,  562,  563,  570,  589,
                                        603,  604,  605,  606,  607,  608,  609,  610,  611,  612,  612,
                                        613,  614,  615,  616,  617,  618,  619,  620,  621,  622,  622,
                                        622,  636,  638,  638,  642,  644,  644,  645,  653,  661,  669,
                                        676,  676,  679,  684,  696,  700,  714,  721,  721,  725,  725,
                                        730,  731,  732,  733,  734,  734,  735,  735,  737,  742,  744,
                                        749,  750,  754,  757,  758,  760,  761,  770,  780,  786,  788,
                                        789,  810,  816,  818,  820,  823,  825,  826,  827,  828,  829,
                                        829,  830,  831,  832,  833,  834,  835,  836,  837,  838,  838,
                                        839,  840,  841,  841,  842,  843,  844,  845,  846,  847,  848,
                                        849,  852,  853,  853,  854,  855,  858,  861,  872,  873,  874,
                                        875,  875,  876,  876,  877,  877,  878,  878,  879,  880,  881,
                                        881,  882,  883,  884,  884,  885,  886,  887,  888,  888,  889,
                                        890,  890,  890,  891,  891,  892,  893,  894,  895,  896,  897,
                                        898,  899,  900,  901,  902,  903,  904,  905,  906,  907,  908,
                                        909,  909,  910,  911,  912,  913,  914,  915,  916,  917,  917,
                                        918,  919,  920,  921,  922,  922,  923,  924,  925,  925,  926,
                                        927,  928,  929,  930,  931,  932,  932,  932,  933,  934,  935,
                                        936,  937,  938,  938,  938,  938,  944,  948,  952,  955,  955,
                                        956,  957,  957,  958,  958,  959,  973,  975,  980, 1000, 1001,
                                       1001, 1001, 1001, 1002, 1002, 1002, 1003, 1003, 1003, 1004, 1004,
                                       1004, 1004, 1004, 1004, 1004, 1005, 1009, 1011, 1014, 1024, 1028,
                                       1028, 1033, 1033, 1041, 1063, 1064, 1065, 1072, 1074, 1077, 1083,
                                       1083, 1084, 1085, 1085, 1086, 1087, 1088, 1088, 1089, 1090, 1090,
                                       1091, 1092, 1093, 1094, 1095, 1098, 1098, 1099, 1100, 1101, 1101,
                                       1102, 1103, 1103, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110,
                                       1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121,
                                       1122, 1123, 1124, 1125, 1125, 1126, 1126, 1126, 1127, 1127, 1127,
                                       1128, 1128, 1129, 1129, 1130, 1130, 1131, 1151, 1152, 1156, 1156,
                                       1157, 1158, 1160, 1170, 1171, 1172, 1173, 1173, 1174, 1176, 1184,
                                       1188, 1204, 1206, 1206, 1208, 1208, 1209, 1210, 1214, 1219, 1223,
                                       1230, 1231, 1232, 1233, 1234, 1234, 1234, 1235, 1235, 1235, 1236,
                                       1236, 1237, 1237, 1238, 1238, 1238, 1239, 1239, 1240, 1240, 1240,
                                       1241, 1242, 1243, 1244, 1245, 1245, 1245, 1246, 1246, 1246, 1247,
                                       1247, 1247, 1247, 1248, 1248, 1248, 1248, 1249, 1249, 1249, 1249,
                                       1250, 1250, 1250, 1250, 1251, 1251, 1251, 1251, 1252, 1252, 1252,
                                       1252, 1253, 1253, 1253, 1253, 1253, 1254, 1254, 1254, 1254, 1254,
                                       1255, 1255, 1255, 1255, 1256, 1256, 1256, 1256, 1257, 1257, 1257,
                                       1257, 1258, 1258, 1258, 1258, 1259, 1259, 1259, 1259, 1260, 1260,
                                       1260, 1260, 1260, 1261, 1261, 1261, 1261, 1262, 1262, 1262, 1262,
                                       1263, 1263, 1263, 1263, 1264, 1264, 1264, 1264, 1265, 1265, 1265,
                                       1265, 1266, 1266, 1266, 1266, 1266, 1267, 1267, 1267, 1267, 1268,
                                       1268, 1268, 1269, 1269, 1269, 1270, 1270, 1270, 1270, 1271, 1271,
                                       1271, 1272, 1272, 1272, 1273, 1273, 1274, 1275, 1276, 1277, 1278,
                                       1279, 1280, 1280, 1288, 1289, 1290, 1291, 1292, 1292, 1293, 1294,
                                       1295, 1296, 1297, 1297, 1298, 1299, 1300, 1300, 1301, 1301, 1301,
                                       1302, 1302, 1303, 1303, 1304, 1304, 1305, 1306, 1306, 1307, 1308,
                                       1309, 1310, 1311, 1312, 1313, 1313, 1314, 1315, 1316, 1317, 1318,
                                       1319, 1319, 1320, 1320, 1320, 1320, 1321, 1321, 1321, 1321, 1321,
                                       1322, 1322, 1322, 1322, 1323, 1323, 1323, 1324, 1324, 1324, 1324,
                                       1325, 1325, 1325, 1326, 1326, 1326, 1327, 1327, 1327, 1328, 1328,
                                       1328, 1328, 1329, 1329, 1329, 1330, 1330, 1330, 1331, 1331, 1331,
                                       1332, 1332, 1332, 1333, 1333, 1333, 1334, 1334, 1334, 1335, 1335,
                                       1335, 1336, 1336, 1336, 1336, 1337, 1337, 1337, 1337, 1338, 1338,
                                       1338, 1338, 1338, 1339, 1339, 1339, 1340, 1340, 1340, 1341, 1342,
                                       1342, 1343, 1344, 1345, 1354, 1355, 1358, 1358, 1360, 1360, 1369,
                                       1378, 1378, 1378, 1402, 1405, 1417, 1421, 1422, 1423, 1424, 1425,
                                       1425, 1426, 1427, 1428, 1428, 1429, 1429, 1430, 1430, 1431, 1431,
                                       1432, 1432, 1433, 1433, 1434, 1434, 1435, 1435, 1436, 1436, 1437,
                                       1437, 1438, 1438, 1439, 1439, 1440, 1440, 1441, 1441, 1442, 1442,
                                       1443, 1443, 1444, 1444, 1445, 1445, 1445, 1446, 1446, 1446, 1447,
                                       1447, 1447, 1448, 1448, 1448, 1448, 1449, 1449, 1449, 1449, 1450,
                                       1450, 1450, 1451, 1451, 1452, 1452, 1453, 1453, 1454, 1454, 1455,
                                       1455, 1456, 1456, 1457, 1457, 1458, 1458, 1459, 1459, 1460, 1460,
                                       1461, 1461, 1462, 1462, 1463, 1463, 1464, 1465, 1466, 1467, 1468,
                                       1469, 1470, 1471, 1478, 1479, 1484, 1500, 1501, 1502, 1503, 1504,
                                       1505, 1506, 1507, 1508, 1509, 1509, 1510, 1511, 1512, 1513, 1514,
                                       1515, 1516, 1517, 1517, 1518, 1519, 1520, 1521, 1521, 1522, 1523,
                                       1523, 1524, 1524, 1525, 1526, 1527, 1527, 1527, 1528, 1529, 1530,
                                       1531, 1531, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540,
                                       1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1548, 1548, 1549,
                                       1550, 1550, 1551, 1551, 1551, 1552, 1553, 1554, 1555, 1556, 1556,
                                       1557, 1557, 1558, 1559, 1560, 1560, 1561, 1562, 1563, 1564, 1565,
                                       1566, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1573, 1574,
                                       1574, 1575, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583,
                                       1584, 1584, 1585, 1585, 1585, 1586, 1587, 1587, 1587, 1588, 1589,
                                       1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599,
                                       1600, 1603, 1605, 1605, 1605, 1606, 1617, 1620, 1634, 1636, 1639,
                                       1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649,
                                       1650, 1650, 1651, 1652, 1653, 1654, 1654, 1655, 1655, 1656, 1656,
                                       1657, 1658, 1659, 1660, 1660, 1661, 1662, 1663, 1664, 1665, 1665,
                                       1666, 1666, 1667, 1667, 1668, 1668, 1669, 1670, 1671, 1672, 1673,
                                       1674, 1675, 1675, 1676, 1677, 1678, 1679, 1680, 1697, 1722, 1729,
                                       1732, 1745, 1746, 2727, 2727, 2807, 2848, 2850, 2854, 2878, 2891,
                                       2892, 2900, 2900, 2931, 2933, 2934, 2934, 2935, 2938, 2975, 2981,
                                       2985, 3009, 3013, 3060, 3104, 3156, 3166, 3227, 3288, 3444],
            'Assignment': ['Glutathione', 'L-arginine ', 'Trp', 'Lysozymes proteins G T',
                           'Cholesterol ester', 'Trp', 'Cholesterol S-S stretching mode',
                           'Proline', 'Proline', 'Tryptophane/cytosine guanine ', 'Amide-VI ',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine', '',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C-C twist aromatic ring of phenylalanine',
                           'C–C twist in phenylalanine (protein) ', 'Protein Phe A',
                           'Phenylalanine Tyrosine', 'Phe', 'L-Tyrosine lactose', 'Tyrosine ',
                           'L-tyrosine lactose', 'Tyr', 'C–C twist in tyrosine',
                           'G ring str.', 'Nucleic acid', 'C–S bond', 'Glutathione',
                           'Nucleic acid', 'CYTc',
                           'CCN Stretch Bending Vinyl & Porphyrin modes', 'Glutathione', 'A',
                           'Met C', 'Cholesterol (C-S trans stretching mode) methionine',
                           'Polysaccharides', 'Nucleic acid', 'DNA/RNA (adenine) protein',
                           'Adenine ', 'Adenine hypoxanthine coenzyme A',
                           'Phosphatidylserine', 'Phosphatidylserine', 'Phosphatidylserine',
                           'Phosphatidylserine', 'A ring br.', 'Phosphatidylserine',
                           'Trp coenzyme A A C T G', 'Phosphatidylserine',
                           'DNA/RNA backbone protein (tyrosine)', 'Phospholipid',
                           'DNA/RNA (bases thymine) protein (tryptophan)',
                           'nucleic acids DNA tryptophan and nucleoproteins',
                           'CH2 rock symmetric breathing of tryptophan', 'Tryp',
                           'C-C stretching mode of tryptophan', 'Tryptophan', 'Trp',
                           'Sym. ring breathing in tryptophane ', '',
                           'Uracil ring breathing (nucleotide) ', 'DNA RNA',
                           'C ring br. T ring br.', 'C U T', 'L-serine',
                           'CCH deformation aliphatic (collagen) ', 'Collagen ',
                           'Structural protein modes of tumors ', 'Tyrosine',
                           'DNA/RNA backbone protein (tyrosine)', 'Tyrosine',
                           'DNA/RNA backbone protein (tyrosine)', 'Tyr', 'Nucleic acid',
                           'tyrosine', 'tyrosine', 'tyrosine', 'tyrosine', 'tyrosine',
                           'tyrosine', 'tyrosine', 'tyrosine', 'tyrosine',
                           'Amine deformation vibrations ', 'tyrosine', 'tyrosine',
                           'tyrosine', 'tyrosine', 'Protein (proline tyrosine)', 'tyrosine',
                           'tyrosine', 'tyrosine', 'tyrosine', 'tyrosine', 'tyrosine',
                           'tyrosine', 'tyrosine', 'Proline tyrosine',
                           'Ring breathing mode of tyrosine C–C stretch of proline ring',
                           'Tyr', 'Ring breathing in tyrosine CCH deformation ',
                           'Protein (collagen)', 'stretching mode of the phosphate group',
                           'Tyrosine collagen',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Tryptophan ',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'CC stretch (protein collagen) ',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Protein (collagen)',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'C-C stretching mode of tryptophan',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Tryptophan',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Pro Val Gly Trp Glu Hyd',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           '',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Amino galactose',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Glutathione', 'Saccharide',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Tyr',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Glutathione',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'C–C stretch (protein collagen) ',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Pro glucose',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Protein (proline valine α-helix)',
                           'Protein (proline valine α-helix)',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'C–C skeletal stretch in protein collagen ', 'Protein (collagen)',
                           'stretching vibrations for the amino acids proline and valine and polysaccharides',
                           'Skeletal str α', 'Protein (proline valine α-helix)',
                           'Single-bond stretching vibrations for the amino acids proline and valine and polysaccharides ',
                           'Protein (proline valine α-helix)', 'CH2 rock',
                           'Protein bands; structural protein modes of tumors',
                           'Protein bands; structural protein modes of tumors',
                           'Lipid protein',
                           'Protein bands; structural protein modes of tumors',
                           'Valine proline',
                           'Protein bands; structural protein modes of tumors',
                           'Sym. stretch phosphate',
                           'deoxygenated of cells porphyrin macrocycle',
                           '"=C-H out-of-plane deformation"', 'Protein',
                           'Protein (phenylalanine)', 'Phenylalanine protein',
                           'Protein (phenylalanine)', 'Protein (phenylalanine)', 'Protein',
                           'Phenylalanine protein', 'Phe', 'Protein',
                           'Sym. ring breathing of phenylalanine ', 'Phenylalanine protein',
                           'Protein', 'Phenylalanine ', 'Phenylalanine Collagen IV I',
                           'Symmetric CC aromatic ring breathing', 'Phenylalanine protein',
                           'phenylalanine',
                           'C─C symmetric ring breathing mode of phenylalanine', 'Protein',
                           'Protein (phenylalanine)', 'Try Lys Phe',
                           'Protein (phenylalanine)', 'Phenylalanine',
                           "2'-deoxyribose phosphate", 'Protein (phenylalanine)', 'Phe',
                           'C–H in plane bending of phenylalanine ',
                           'Phenylalanine tryptophan tyrosine', 'Protein (phenylalanine)',
                           'Phe', 'C–C skeletal stretch in lipids ', '', 'Collagen',
                           'Phospholipids ', 'Lipids nucleic acids proteins carbohydrates',
                           'Nucleic acid (DNA RNA)', 'Phospholipids O-P-O and C-C',
                           'Nucleic acid (DNA RNA)', 'Nucleic acid (DNA RNA)',
                           'phosphodiester groups in nucleic acids', 'Nucleic acid (DNA RNA)',
                           'Nucleic acid (DNA RNA)',
                           'Protein phospholipid glycogen Collagen IV I',
                           'Nucleic acid (DNA RNA)', 'Nucleic acid (DNA RNA)',
                           'Nucleic acid (DNA RNA)',
                           'Symmetric phosphate stretching vibrations',
                           'Nucleic acid (DNA RNA)', 'Nucleic acid (DNA RNA)',
                           'Nucleic acid (DNA RNA)', 'Nucleic acid (DNA RNA)',
                           'Nucleic acid (DNA RNA)',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'phosphate str.',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'DNA: O–P–O backbone stretch ',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'Phenylalanine', 'Phe',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'C–C skeletal stretch in lipids',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'Phospholipid lipoproteins C-C skeletal of acyl backbone in lipid',
                           'Protein Phospholipid C-C str',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'Protein Lipid', '', 'Lipids',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'CC stretch CC skeletal stretch trans PO2 symmetric',
                           'saturated fatty acids',
                           'CC stretch CC skeletal stretch trans PO2 symmetric', 'D-mannose',
                           'D-Mannose ', 'Protein carotenoid', 'Protein carotenoid',
                           'β-carotene', 'CH3 rock', 'Carotenoids',
                           'C-C stretching mode of beta-carotene', 'β-carotene',
                           'Protein (tyrosine)', 'Phenylalanine tyrosine ', 'CH3 rock',
                           'Tyrosine hemoglobin Flavin', 'Phenylalanine tyrosine (protein)',
                           'Trp Phe', 'Cytosine/guanine/adenine ', '',
                           'C ring str. T ring str.',
                           'Protein (phenylalanine tryptophan tyrosine)', 'Tyrosine',
                           'Tyrosine', 'CC stretch backbone phenyl ring ', 'Trp',
                           'Tryptophan phenylalanine (protein)', 'Amide III',
                           'Homo polypeptide', 'Protein (β-sheet)', 'Amide III', '', '', '',
                           '', '', 'Amide III ', 'Amide III', '', 'Protein (β-sheet)',
                           'Amide III', '', 'Amide III', '', 'Amide III', '',
                           'Protein (β-sheet)', 'Amide III', '', 'Amide III', '',
                           'C ring str. A ring str.', 'Amide III', 'Amide III', 'Amide III',
                           'Amide III', 'Amide III', '', '', 'Amide III', '', '', 'Amide III',
                           'Amide III: β-sheet ', '', '', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'C-O4 aromatic stretching ', 'Amide III parallel beta-sheet',
                           'Amide III', '', '', ' Protein (β-sheet)',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III (C–N stretch + N–H bend)',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', '', '',
                           'Amide III parallel beta-sheet', 'Amide III', 'Protein', '', '',
                           'DNA/RNA (thymine adenine) protein (α-helix)', 'Amide III', '', '',
                           'Amide III', 'Amide III (collagen assignment)', '', '',
                           'Amide III', '', '', 'Amide III', '', '', 'C A', 'Amide III', '',
                           '', 'Amide III', '', '', 'Amide III', 'deformation=CH amide III ',
                           'Amide III', 'Amide III', 'Amide III', 'Amide III', 'Amide III',
                           'Amide III', 'Amide III',
                           'Phospholipid amide III proteins lipids T', 'Amide III', '', '',
                           '', '', '', 'Cytosine', '', '', '', '', '', 'Lipid', '', '', '',
                           'Trp α helix Phospholipids', 'Collagen IV I', '',
                           'Trp α helix Phospholipids', '', 'Trp α helix Phospholipids', '',
                           'Trp α helix Phospholipids', '', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids',
                           'Amide III (N–H) α-helix C-C Str & C-H bending',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', '', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Collagen assignment; Amide III', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Collagen assignment; Amide III',
                           'CH2 deformation in lipids/adenine/cytosine amide III (α-helix)',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Collagen assignment; Amide III',
                           'Collagen tryptophan', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Collagen and purine bases of DNA ',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Lipids CH vibration in DNA/RNA', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'A', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'CH3CH2 wagging vibrations of collagen',
                           'Trp α helix Phospholipids', 'Protein A and G of DNA/RNA ',
                           'CH2 deformation', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Unsaturated fatty acid', 'Protein nucleic acid',
                           'Trp α helix Phospholipids', 'Unsaturated fatty acid',
                           'Protein nucleic acid', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Polynucleotide chain (DNA/RNA) ',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'Trp α helix Phospholipids', 'Trp α helix Phospholipids',
                           'G ring str.', 'Collagen (protein assignment)\r',
                           'Trp. mitochondria CYTc ', 'CH3-(C=O) strong than hydrocarbons',
                           'Tryptophan', '', 'Trp porphyrins lipids G T protein',
                           'T A G of DNA ', 'CH3 in-phase deformation', 'G A T',
                           'Phospholipids', 'Glutathione', 'C=C stretching in quinoid ring ',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending (CH)3 out-of-phase deformation', 'CH3 deformation',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'lipids and proteins', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'CH2 bending mode of proteins lipids and some amino acid',
                           'Lipid protein ', 'CH2 bending (CH)3 out-of-phase deformation',
                           'Collagen phospholipids', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Protein Lipid',
                           'Collagen (protein assignment)', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation',
                           'Phospholipid C-H scissor in CH2', 'Collagen (protein assignment)',
                           'CH2 deformation in lipids', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'CH2 bending (CH)3 out-of-phase deformation', 'Lipid protein ',
                           'Lipid protein ', 'Lipid protein ', 'Lipid protein ',
                           'Lipid protein ', 'Lipid protein ', 'Lipid protein ',
                           'Lipid protein ', 'DNA/RNA (adenine guanine)\r', 'Amide II',
                           'C A T', 'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', '',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'β-carotene accumulation ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Amide II shift to 1548',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'β-carotene',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'C = C stretching mode of beta-carotene',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'Carotenoid',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Carotenoid absent from normal tissues ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Trp cytochrome c δ and ν coupled out-of-phase NADH',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Amide II in plane N-H bending',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'C G',
                           'Tryptophane ', 'parallel β-sheet protein tryp. carotenoid ', '',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'Trp',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Amide II (N–H bend + C–N stretch)',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'Tryptophan ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Amide I (C=O stretch)',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'DNA/RNA bases ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', '',
                           'parallel β-sheet protein tryp. carotenoid ', 'A ring str.',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'Acetoacetate',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Unsaturated fatty acid',
                           'CN2 scissoring and NH2 rock of mitochondria and phosphorylated proteins',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'Trp mitochondria NADH',
                           'parallel β-sheet protein tryp. carotenoid ', 'Protein Tyr',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'C-C stretching C-H bending',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ',
                           'parallel β-sheet protein tryp. carotenoid ', 'Tyr Phe',
                           'Phe. tyr.', 'CO stretching C=C bending', 'Phenylalanine tyrosine',
                           'C=C phenylalanine ', 'Porphyrin and tryptophan',
                           'Tyr Trp C=C str', 'Amide I', 'carboxyl vibration', 'protein',
                           'Amide I in α-helix', 'Protein', 'Protein', 'Protein', 'Protein',
                           'Protein', 'Protein', 'Protein', 'Protein', 'Protein', 'Protein',
                           'Protein', '', 'Protein', 'Protein', 'Protein', 'Protein',
                           'Proteins Amide I α helix Phospholipids', 'Amide I α-helix ',
                           'Protein', 'Amide I unordered', 'Protein', 'Protein', 'Protein',
                           'Protein', 'Protein', 'Amide I', 'Protein', 'Protein', 'Protein',
                           'Protein', 'Amide I: α helix ', 'Protein', 'Protein',
                           'Protein (α-helix) lipid (fatty acid) DNA/RNA (thymine)',
                           'Salt environment effect Unordered or random structure Collagen IV I',
                           'Protein', 'Protein', 'Structural protein modes of tumors',
                           'Protein', 'Protein', 'Protein', 'Protein', 'Protein', 'Protein',
                           'Protein', 'C = O stretching mode amide I α-helix', 'Protein',
                           'Protein', 'Protein', 'Protein', 'Protein',
                           'Protein (α-helix) lipid (fatty acid) DNA/RNA (thymine)',
                           'ester group3', 'Ester group', 'Lipids phospholipids ',
                           'C=O group of lipids and lipids esters.', 'C=O Stretch', '',
                           '1378 cm bend overtone', 'Aliphatic -N-CH3 amine',
                           'C–H bonds of lipids glycogen proteins RNA and DNA.',
                           'Poly methylene chain F', 'CH2 Stretch', 'CH2 sym. Stretch',
                           'Poly methylene chain', 'CH2 Stretch FR Stretch', 'CH stretch ',
                           'CH3 strong symmetric str.', 'Proteins', 'CH3 Stretch FR Stretch',
                           'P.F.', 'CH3 Stretch FR Stretch', 'CH3 Stretch FR Stretch',
                           'CH2 asym. and CH3 sym. stretch CH3 sym. (lipid) ',
                           'CH3 asym. Stretch ', 'CH3 asym. Stretch',
                           'CH3 medium asymmetric str.',
                           'C–H bonds of lipids glycogen proteins RNA and DNA.', 'CH3-(C=O)',
                           '', '', '', 'O-H Stretch water band', 'O-H Stretch water band', '',
                           ''],
            'Vibrational mode': ['', 'S─S stretching', '', '', '', '', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', 'C─C─C ring in-plane', '', '', '', '',
                                   '', '', '', '', '', '', '',
                                   'C-C  bending deformed swing (Twisted) phenylalanine', '', '',
                                   'C─S  stretching', 'C-S twist vibration', '', '', '', 'dC', '', '',
                                   'dT', 'stretch  bending  (CCN) Vinyl & Porphyrin ', '', '', '', '',
                                   '', '', 'dA', 'Ring breathing mode C─S',
                                   'C─H  in-plane deformation', 'C-H bending vibration', '', '', '',
                                   '', '', '', '', '', 'Ring breathing mode C─S', '',
                                   'Ring breathing mode', '', '', 'CH2 Rock Sym. breathing ', '',
                                   'symmetric stretch (Indole ring breathing)', '', '',
                                   'C─H out of plane bend', '', 'PO2- group symmetric stretch', '',
                                   '', 'C-C-O stretching vibration', '', 'C─C  stretching', '',
                                   'Ring breathing ', 'O─P─O stretch ring breathing', '',
                                   'O─P─O stretch ring breathing', '', 'PO2- asymmetric stretch', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '',
                                   'C─C stretch ring breathing', '', '', '', '', '', '', '', '', '',
                                   '', '', '', 'C-C Proline stretch', '', '', '', '', '', '', '', '',
                                   '', 'C-C Hydroxyproline stretch', '', '', '', '', '',
                                   'ring  in-plane deformation', '', '', '', '', '', '', '', '', '',
                                   '', '', 'C-O-H scissoring vibration', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', 'C-C stretch', 'C─C stretch', '',
                                   '', '', '', '', '', 'C-C Proline and valine (a-helix) stretch', '',
                                   '', 'C─C stretch', '', 'C─C stretch', '', '', '',
                                   'CH3 (deformed) bending swing', '', 'C-C vibration', '', '',
                                   '═C─H out of plane deformation C─C Asym. Str. ', '', '',
                                   'Symmetric ring breathing', 'ring breathing stretch',
                                   'Symmetric ring breathing', 'Symmetric ring breathing', '',
                                   'ring breathing stretch', '', '', '', 'ring breathing stretch', '',
                                   'C─C  symmetric stretching',
                                   'Symmetric CC aromatic ring breathing ', '',
                                   'ring breathing stretch', '', '', '', 'Symmetric ring breathing',
                                   '', 'Symmetric ring breathing', 'C-H stretching vibration', '',
                                   'C─H stretch', '', '', 'C-H (Plane bending) aromatic compound',
                                   'C─H stretch', '', '', '-C = C = C- stretch', '',
                                   'C─C  stretching', '',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch', '',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch', '',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'CC stretch CC skeletal stretch trans PO2 symmetric ',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch', '',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch',
                                   'O-P-O- symmetric stretch C-C phospholipid stretch', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                   '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                   'C-N protein stretch C-C lipid stretch', 'C─H in-plane bend',
                                   'C─C stretching trans ', '', '', '', '',
                                   'C-N stretching vibration', 'C─C  stretching',
                                   'C─N and C─C stretch', 'C─N and C─C stretch', 'C═C stretch ', '',
                                   'Polyene chain', '', '', 'C─H bend', '', '',
                                   'C─H in-plane bending ', 'C-H stretch', '', '',
                                   'C─H in-plane bend', '', 'C − C6H5 stretch', 'Ring vibration ', '',
                                   '', '', 'C-C6H5 stretch',
                                   'C-N stretching vibration N-H bending vibration', 'Amide III ',
                                   'Amide III', '', 'Amino compound III (β fold)',
                                   'Amino compound III (β fold)', 'Amino compound III (β fold)',
                                   'Amino compound III (β fold)', 'Amino compound III (β fold)', '',
                                   '', 'Amino compound III (β fold)', 'Amide III', '',
                                   'Amino compound III (β fold)', '', 'Amino compound III (β fold)',
                                   '', 'Amino compound III (β fold)', 'Amide III', '',
                                   'Amino compound III (β fold)', '', 'Amino compound III (β fold)',
                                   '', '', '', '', '', '', 'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', 'Amide III', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'C-H stretch H-N- : bending deformed swing (Bending) amino compound III',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', 'Amide III', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '',
                                   'Amino compound III (a-helix)',
                                   'Amino compound III (random coil corner', '', '', '', '', '', '',
                                   '', '', '', '', '', 'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending', '',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending', 'Fatty acid',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending',
                                   'Lipid CH2 bending and CH2CH3 bending', '',
                                   'Amide III  bending(N─H)-30% α-helix stretch (C─N)-40% & CH3  bending',
                                   'Lipid CH2 bending and CH2CH3 bending', '',
                                   'Lipid CH2 bending and CH2CH3 bending', '',
                                   'Lipid CH2 bending and CH2CH3 bending', '',
                                   'Lipid CH2 bending and CH2CH3 bending', '', '', '', '', '', '', '',
                                   '', '', '', 'N─H in-plane bend', '', '', '', '', '', '', '', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '',
                                   'CH3CH2 twisting ',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', 'CH2 twist vibration',
                                   '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '',
                                   'CH2 Deformation ', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '',
                                   'C-H bending deformed swing (Plane deformation) ordinary olefin',
                                   'CH2CH3 stretch and bending deformed swing', '', '', '', '', '',
                                   '', '', '', '', 'CH3─(C═O)', '', '', 'C─C aromatic stretching', '',
                                   'CH3 in-phase deformation ', '', '', 'C─C  stretching', '', '', '',
                                   '', '', '', '', '', '', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   'bυ(C-H2 )',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   'CH2 bending deformed swing', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '', '',
                                   '', '', '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '', '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ', '',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   '(CN) bending (CH)3  bending out-of-phase deformation ',
                                   'Ring breathing mode', '', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', 'C─C aromatic stretching',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', 'C-C stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II in plane (N─H) bending: 60%;  (C─N)stretch:40%;',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '', '',
                                   'Amide II Shift to 1548 (C═C) stretch', '-NO2 asymmetric stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', 'C─C6H5 stretching',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', 'N─H in-plane bend',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', 'C=C bending vibration',
                                   'Amide II Shift to 1548 (C═C) stretch', 'C=C Lipid stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'C─C stretching C─H bending ',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch',
                                   'Amide II Shift to 1548 (C═C) stretch', '',
                                   'CO stretching C═C bending ', '', 'C=C Aromatic compound stretch',
                                   '', 'C=C stretch', '', '', '', 'Amide I in α-helix', '',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'C─C aromatic stretching ',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix', '',
                                   'C═O stretching', 'Amino compounds I a helix', '',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix',
                                   'C=C stretching vibration:(β-pleated sheet)',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix', '',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'C═O stretch Amide I', 'Amide I β-sheet stretch(C═O) 80%',
                                   'Amino compounds I a helix', 'Amino compounds I a helix', '',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', '', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'Amino compounds I a helix', 'Amino compounds I a helix',
                                   'C═O stretch amide I', '', '', ' (C═C) stretch', '', '',
                                   '1378 cm−1 bend overtone ', '', '', '', 'CH2 stretch', '', '',
                                   'CH2 FR stretch', '', '', '', '', '', 'CH3 FR stretch', '', '', '',
                                   '', '', '', '', '', 'CH3─(C═O)', '(O─H) water band stretch',
                                   '(O─H) water band stretch', '', '', 'O─H Liquid water',
                                   'O─H Liquid water '],
            'Strength' : ['', 'strong', '', '', 'weak', '', '', '', '', 'broad',
                           ' weak shoulder', '', '', '', '', '', '', '', '', '',
                           ' very strong', '', '', '', '', '', '', '', '', '', 'weak', '', '',
                           '', '', 'very strong', '', '', 'very weak', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', 'weak', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', 'very weak', ' strong',
                           'very weak', '', '', '', '', 'medium', 'weak', '', ' medium', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', 'strong', '',
                           '', '', '', '', '', '', '', 'medium( shoulder)', '', '', '', '',
                           '', '', '', ' medium', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', 'medium', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', 'strong', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', 'weak(shoulder)', '', '', '', '', '',
                           '', '', '', '', '', '', 'very strong', '', '', ' medium', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', 'medium', '', '', '',
                           'weak', '', '', 'weak', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', 'medium', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', 'weak', '', '', '', '', '', '', ' medium',
                           '', '', '', '', '', '', 'strong', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', 'weak', ' medium', '', '', ' medium', '',
                           'weak', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', 'strong', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', 'weak', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', ' medium', '', '', '', '', '', '', '', '', '', '',
                           '', '', 'strong', '', '', '', '', ' mediumshoulder', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', 'strong', '', '', '', '',
                           '', '', '', '', ' mediumbroad', ' very strong', '', '', '', '',
                           ' mediumshoulder', '', '', '', '', '', '', 'shoulder', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           'very strong', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', ' very strong', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', 'weak', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', 'weak', '', '', ' medium', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', 'weak', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', ' very strong',
                           '', '', '', '', '', 'strong', '', '', '', '', '', '', '', '', '',
                           '', '', '', 'very strong', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                           '', '', '', '', '', 'strong', '', '', 'medium', '', '', '', '', '',
                           '', 'very strong', 'medium', 'medium', '', '', '', '', '', '', '',
                           '', '', ''],
            'PMID': [36239879, 21747512, 36239879, 22502575, 20223058, 36239879,
                       36227878, 36832007, 36832007, 20223058, 21747512, 36227878,
                       36227878, 36227878, 36227878, 36227878, 36227878, 36227878,
                       36227878, 36227878, 29981226, 36227878, 36227878, 36227878,
                       36227878, 36227878, 36227878, 36227878, 36227878, 36227878,
                       20223058, 22502575, 24710050, 36239879, 36832007, 21747512,
                       30666105, 36239879, 20223058, 30899639, 24710050, 36832007,
                       36239879, 24710050, 23154776, 23448574, 36832007, 30899639,
                       22502575, 36227878, 36239879, 24710050, 34743445, 21747512,
                       30666105, 36832007, 36832007, 36832007, 36832007, 30899639,
                       36832007, 22502575, 36832007, 34743445, 36239879, 34743445,
                       32531903, 23448574, 23154776, 36227878, 24710050, 36239879,
                       20223058, 29981226, 20223058, 24710050, 30899639, 22502575,
                       30666105, 20223058, 21747512, 32508914, 21747512, 34743445,
                       32508914, 34743445, 36239879, 24710050, 32531903, 32531903,
                       32531903, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 32508914, 32531903, 32531903, 32531903, 32531903,
                       34743445, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 32531903, 32531903, 32508914, 36227878, 36239879,
                       20223058, 24710050, 32531903, 32508914, 32531903, 32531903,
                       32531903, 32508914, 32531903, 20223058, 32531903, 24710050,
                       32531903, 32531903, 36227878, 32531903, 32531903, 21747512,
                       32531903, 32531903, 32531903, 22502575, 32531903, 32531903,
                       32531903, 32531903, 32531903, 36832007, 32531903, 30666105,
                       32531903, 36239879, 32508914, 32531903, 32531903, 32531903,
                       32531903, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 32531903, 32531903, 22502575, 32531903, 32531903,
                       32531903, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 36239879, 32531903, 32531903, 32531903, 32531903,
                       20223058, 32531903, 32531903, 32531903, 22502575, 32531903,
                       32531903, 32531903, 32531903, 32531903, 32531903, 32531903,
                       32531903, 34743445, 34743445, 32531903, 32531903, 32531903,
                       32531903, 32531903, 20223058, 24710050, 32531903, 36239879,
                       34743445, 32508914, 34743445, 36239879, 36832007, 36832007,
                       24710050, 36832007, 30666105, 36832007, 20223058, 23154776,
                       23448574, 36832007, 34743445, 24710050, 34743445, 34743445,
                       36832007, 24710050, 36239879, 36832007, 20223058, 24710050,
                       36832007, 21747512, 23154776, 23448574, 24710050, 32531903,
                       36227878, 36832007, 34743445, 22502575, 34743445, 30666105,
                       30899639, 34743445, 36239879, 20223058, 24710050, 34743445,
                       36239879, 20223058, 24710050, 36832007, 21747512, 22502575,
                       24710050, 36239879, 24710050, 24710050, 32531903, 24710050,
                       24710050, 23154776, 24710050, 24710050, 24710050, 36832007,
                       24710050, 24710050, 24710050, 24710050, 24710050, 23448574,
                       30899639, 23448574, 23448574, 20223058, 23448574, 23448574,
                       23448574, 32508914, 36239879, 23448574, 23448574, 23448574,
                       23448574, 23448574, 23448574, 23448574, 23448574, 23448574,
                       23448574, 23448574, 23448574, 23448574, 23448574, 23448574,
                       23448574, 23448574, 23448574, 23448574, 23448574, 23448574,
                       20223058, 23448574, 23448574, 36227878, 36239879, 23448574,
                       24710050, 29981226, 23154776, 23448574, 23448574, 32531903,
                       23448574, 30666105, 21747512, 34743445, 34743445, 23154776,
                       23448574, 24710050, 36227878, 36239879, 34743445, 32508914,
                       23448574, 23154776, 24710050, 36239879, 20223058, 29981226,
                       30899639, 34743445, 21747512, 32508914, 20223058, 36239879,
                       24710050, 30666105, 23154776, 34743445, 23448574, 24710050,
                       24710050, 24710050, 24710050, 24710050, 32508914, 36239879,
                       24710050, 34743445, 36239879, 24710050, 36239879, 24710050,
                       36239879, 24710050, 34743445, 36239879, 24710050, 36239879,
                       24710050, 30899639, 36239879, 36239879, 36239879, 36239879,
                       36239879, 24710050, 24710050, 36239879, 24710050, 24710050,
                       36239879, 20223058, 24710050, 24710050, 36239879, 24710050,
                       24710050, 36227878, 36239879, 24710050, 24710050, 36227878,
                       36239879, 24710050, 24710050, 36227878, 36239879, 24710050,
                       24710050, 36227878, 36239879, 24710050, 24710050, 36227878,
                       36239879, 24710050, 24710050, 32508914, 36227878, 36239879,
                       24710050, 24710050, 34743445, 36227878, 36239879, 24710050,
                       24710050, 36227878, 36239879, 24710050, 24710050, 36227878,
                       36239879, 24710050, 24710050, 36227878, 36239879, 24710050,
                       24710050, 36227878, 36239879, 24710050, 24710050, 36227878,
                       36239879, 24710050, 24710050, 32531903, 36227878, 36239879,
                       24710050, 24710050, 36227878, 36239879, 24710050, 24710050,
                       36227878, 36239879, 24710050, 24710050, 36227878, 36239879,
                       24710050, 24710050, 36227878, 36239879, 24710050, 24710050,
                       36227878, 36239879, 24710050, 24710050, 24710050, 34743445,
                       36239879, 24710050, 24710050, 36239879, 36832007, 24710050,
                       24710050, 36239879, 24710050, 24710050, 36239879, 24710050,
                       24710050, 30899639, 36239879, 24710050, 24710050, 36239879,
                       24710050, 24710050, 36239879, 20223058, 36239879, 36239879,
                       36239879, 36239879, 36239879, 36239879, 36239879, 22502575,
                       36239879, 24710050, 24710050, 24710050, 24710050, 24710050,
                       32508914, 24710050, 24710050, 24710050, 24710050, 24710050,
                       34743445, 24710050, 24710050, 24710050, 36239879, 23154776,
                       24710050, 36239879, 24710050, 36239879, 24710050, 36239879,
                       24710050, 36239879, 36239879, 23448574, 36239879, 36239879,
                       36239879, 36239879, 36239879, 36239879, 36239879, 29981226,
                       36239879, 36239879, 36239879, 36239879, 36239879, 36239879,
                       36239879, 36832007, 24710050, 24710050, 36239879, 36832007,
                       20223058, 24710050, 24710050, 36239879, 36832007, 21747512,
                       24710050, 24710050, 36239879, 24710050, 24710050, 36239879,
                       24710050, 24710050, 32508914, 36239879, 24710050, 24710050,
                       36239879, 24710050, 24710050, 36239879, 24710050, 24710050,
                       36239879, 24710050, 24710050, 30666105, 36239879, 24710050,
                       24710050, 36239879, 24710050, 24710050, 36239879, 24710050,
                       24710050, 36239879, 24710050, 24710050, 36239879, 24710050,
                       24710050, 36239879, 24710050, 24710050, 36239879, 24710050,
                       24710050, 36239879, 24710050, 24710050, 30899639, 36239879,
                       24710050, 24710050, 32531903, 36239879, 23154776, 23448574,
                       24710050, 24710050, 36239879, 24710050, 24710050, 36239879,
                       24710050, 24710050, 36239879, 36239879, 20223058, 36239879,
                       36239879, 36239879, 36239879, 30899639, 36832007, 23154776,
                       23448574, 21747512, 29981226, 22502575, 23154776, 23448574,
                       30899639, 21747512, 36239879, 32508914, 23448574, 23448574,
                       23448574, 23448574, 20223058, 23448574, 23448574, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       32531903, 23154776, 23448574, 36227878, 23154776, 23448574,
                       30666105, 23154776, 23448574, 24710050, 36832007, 23154776,
                       23448574, 36239879, 36832007, 20223058, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23448574, 23154776, 23448574,
                       23154776, 23448574, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 34743445, 32508914,
                       30899639, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 23154776, 29981226,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 32508914, 23154776, 23154776, 23154776,
                       23154776, 23448574, 23154776, 23154776, 36239879, 23154776,
                       36227878, 23154776, 23154776, 23154776, 23154776, 24710050,
                       23154776, 23154776, 23154776, 23154776, 32508914, 23154776,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23448574,
                       23154776, 23154776, 30899639, 20223058, 23154776, 24710050,
                       23154776, 23154776, 23154776, 23154776, 23154776, 36239879,
                       23154776, 32531903, 23154776, 23154776, 23154776, 32508914,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23154776,
                       32531903, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 21747512, 23154776, 23154776, 29981226, 23154776,
                       30899639, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 30666105, 23154776,
                       24710050, 32531903, 23154776, 23154776, 23154776, 36239879,
                       23154776, 23154776, 23448574, 23154776, 23154776, 23154776,
                       23154776, 23154776, 23154776, 23154776, 23154776, 23154776,
                       23154776, 23154776, 36239879, 23154776, 23448574, 24710050,
                       20223058, 24710050, 36239879, 32508914, 30899639, 23154776,
                       23448574, 24710050, 24710050, 24710050, 24710050, 24710050,
                       24710050, 24710050, 24710050, 24710050, 24710050, 24710050,
                       29981226, 24710050, 24710050, 24710050, 24710050, 36239879,
                       21747512, 24710050, 23448574, 24710050, 24710050, 24710050,
                       24710050, 24710050, 30666105, 24710050, 24710050, 24710050,
                       24710050, 20223058, 24710050, 24710050, 34743445, 23154776,
                       24710050, 24710050, 36832007, 24710050, 24710050, 24710050,
                       24710050, 24710050, 24710050, 24710050, 36227878, 24710050,
                       24710050, 24710050, 24710050, 24710050, 34743445, 22502575,
                       32508914, 23154776, 32531903, 23448574, 23154776, 23448574,
                       23448574, 32531903, 23154776, 23448574, 20223058, 23154776,
                       23448574, 20223058, 23448574, 32531903, 23448574, 23154776,
                       23448574, 23448574, 20223058, 20223058, 20223058, 23448574,
                       32531903, 23448574, 23154776, 23154776, 23154776, 23448574,
                       23448574, 23154776, 23154776]
                        }

        raman_peaks_df = pd.DataFrame(raman_peaks_data)

        filtered_df = raman_peaks_df[
            (raman_peaks_df['Raman peaks (cm−1)'] >= start_val) &
            (raman_peaks_df['Raman peaks (cm−1)'] <= end_val)
        ]

        model = PandasTableModel(filtered_df)
        self.tableView_2.setModel(model)

        self.tableView_2.resizeColumnsToContents()

    def updateTooltip(self, event):
        
        pos = event 
        view = self.graphwidget_3.plotItem.vb   
        if self.graphwidget_3.sceneBoundingRect().contains(pos):
            mousePoint = view.mapSceneToView(pos)
            x_coord = mousePoint.x()
            y_coord = mousePoint.y()
            
            tooltip_msg = f"X: {x_coord:.2f}, Y: {y_coord:.2f}"  
            QtWidgets.QToolTip.showText(self.graphwidget_3.mapToGlobal(QtCore.QPoint(pos.x(), pos.y())), tooltip_msg, self.graphwidget_3)
        else:
            QtWidgets.QToolTip.hideText()

##파일첨부1
    def load_file_1(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            df = pd.read_csv(file_path)
            self.getData_1(df)

    def getData_1(self, df):
        # 빈 리스트
        list1 = []

        # 소수점 둘째 자리까지 반올림
        df = df.round(2)

        # 첫번째 행 읽기
        col1 = df.columns

        # X축 데이터
        #x1 = df1[self.col1[0]]
        x1 = df[col1[0]].replace('[\$,]', '', regex=True).astype(float)
        
        # Raw - Y좌표
        for i in range(1,len(col1)):
            colName = f'ROI {i} []'
            #df1[colName] = df1[colName].replace('[\$,]', '', regex=True).astype(float)
            list1.append(colName)

        # Y좌표 평균값
        for i in list1:
            df[list1] = df[list1].replace('[\$,]', '', regex=True).astype(float)
        y1 = df[list1].mean(axis=1).values

        # 베이스라인 조정
        baseObj1 = BaselineRemoval(y1)
        Zhangfit_output1 = baseObj1.ZhangFit()
        
        # 그래프 그리기
        self.graphwidget_1.addLegend(offset=(10,5))
        self.graphwidget_1.plot(x1, y1, pen=pg.mkPen('b', width=2), name='Raw')
        self.graphwidget_1.plot(x1, Zhangfit_output1, pen=pg.mkPen('r', width=2), name='BaslineCorrection')
        #self.graph_1(x1, Zhangfit_output1)


    def graph_1(self,x,y):
        # 그래프 그리기
        #plt.figure(figsize=(10,12))
        #plt.plot(x1, Zhangfit_output1, label='Raw', color='blue')
        self.graphwidget_1.plot(x, y)


##파일첨부2
    def load_file_2(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            df = pd.read_csv(file_path)
            self.getData_2(df)

    def getData_2(self, df):
        # 빈 리스트
        list1 = []

        # 소수점 둘째 자리까지 반올림
        df = df.round(2)

        # 첫번째 행 읽기
        col1 = df.columns

        # X축 데이터
        #x1 = df1[self.col1[0]]
        x1 = df[col1[0]].replace('[\$,]', '', regex=True).astype(float)
        
        # Raw - Y좌표
        for i in range(1,len(col1)):
            colName = f'ROI {i} []'
            #df1[colName] = df1[colName].replace('[\$,]', '', regex=True).astype(float)
            list1.append(colName)

        # Y좌표 평균값
        for i in list1:
            df[list1] = df[list1].replace('[\$,]', '', regex=True).astype(float)
        y1 = df[list1].mean(axis=1).values

        # 베이스라인 조정
        baseObj1 = BaselineRemoval(y1)
        Zhangfit_output1 = baseObj1.ZhangFit()

        # 그래프 그리기
        self.graphwidget_2.addLegend(offset=(10,5))
        self.graphwidget_2.plot(x1, y1, pen=pg.mkPen('b', width=2), name='Raw')
        self.graphwidget_2.plot(x1, Zhangfit_output1, pen=pg.mkPen('r', width=2), name='BaslineCorrection')

        #self.graph_2(x1, Zhangfit_output1)

    def graph_2(self,x,y):
        # 그래프 그리기
        #plt.figure(figsize=(10,12))
        #plt.plot(x1, Zhangfit_output1, label='Raw', color='blue')
        self.graphwidget_2.plot(x, y)


##파일첨부3
    def load_file_3(self):
        if hasattr(self, 'data_loaded_3') and self.data_loaded_3:
            #중복 첨부 방지
            return
        
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            df1 = pd.read_csv(file_path)
            #self.getData_3(df)
            self.load_file_4(df1)
            self.data_loaded_3 = True  # 데이터 첨부 완료

##파일첨부4
    def load_file_4(self, df1):
        if hasattr(self, 'data_loaded_4') and self.data_loaded_4:
            #중복 첨부 방지
            return
        
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            df2 = pd.read_csv(file_path)
            #self.getData_4(df)
            self.getData_4(df1, df2)
            self.data_loaded_4 = True  # 데이터 첨부 완료

#데이터 2개 그래프 그리기
    def getData_4(self, df1, df2):
        # 빈 리스트
        list1 = []
        list2 = []

        # 소수점 둘째 자리까지 반올림
        df1 = df1.round(2)
        df2 = df2.round(2)

        # 첫번째 행 읽기
        col1 = df1.columns
        col2 = df2.columns

        # X축 데이터
        #x1 = df1[self.col1[0]]
        x1 = df1[col1[0]].replace('[\$,]', '', regex=True).astype(float)
        x2 = df2[col2[0]].replace('[\$,]', '', regex=True).astype(float)
                
        # Raw - Y좌표
        for i in range(1,len(col1)):
            colName = f'ROI {i} []'
            #df1[colName] = df1[colName].replace('[\$,]', '', regex=True).astype(float)
            list1.append(colName)

        # UR2 - Y좌표
        for i in range(1,len(col2)):
            colName = f'ROI {i} []'
            #df1[colName] = df1[colName].replace('[\$,]', '', regex=True).astype(float)
            list2.append(colName)

        # Raw - Y좌표 평균값
        for i in list1:
            df1[list1] = df1[list1].replace('[\$,]', '', regex=True).astype(float)
        y1 = df1[list1].mean(axis=1).values

        # UR2 - Y좌표 평균값
        for i in list2:
            df2[list2] = df2[list2].replace('[\$,]', '', regex=True).astype(float)
        y2 = df2[list2].mean(axis=1).values

        # 베이스라인 조정
        baseObj1 = BaselineRemoval(y1)
        baseObj2 = BaselineRemoval(y2)
        Zhangfit_output1 = baseObj1.ZhangFit()
        Zhangfit_output2 = baseObj2.ZhangFit()

        # 그래프 그리기
        self.graphwidget_3.addLegend(offset=(10,5))
        self.graphwidget_3.plot(x1, Zhangfit_output1, pen=pg.mkPen('b', width=2), name='First')
        self.graphwidget_3.plot(x2, Zhangfit_output2, pen=pg.mkPen('r', width=2), name='Second')

        # 데이터프레임 출력
        self.data_value(x1, Zhangfit_output1, Zhangfit_output2)

        # peak 점 표시 함수 호출
        self.peak(x1, x2, Zhangfit_output1, Zhangfit_output2)


## 데이터 프레임 출력
    def data_value(self, x, y1, y2):
        # wavelength 리스트 정수 변환
        x_int = list(map(int, x))

        # Dataframe for the difference value
        df_change = pd.DataFrame({
            'Wavelength' : x_int,
            'ChangeValue' : y1-y2
        })

        ChangeValue = y1 - y2

        model = PandasTableModel(df_change)
        #model = PandasTableModel(pd.DataFrame({'Wavelength': x_int, 'Change Value': ChangeValue}))

        self.tableView_1.setModel(model)
        self.tableView_1.verticalHeader().setDefaultSectionSize(30)
        self.tableView_1.horizontalHeader().setDefaultSectionSize(80)
        self.tableView_1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView_1.show()


        # Dataframe for the difference value
        df_change = pd.DataFrame({
            'Wavelength': x_int,
            'ChangeValue': ChangeValue
        })


        # Save the DataFrame as an instance variable for later use
        self.df_change = df_change

        # Set the initial data in tableView_1
        model = PandasTableModel(df_change)
        self.tableView_1.setModel(model)

        # Save the reference to the model for later use
        self.tableView_1_model = model


## peak 점 출력
    def peak(self, x1, x2, y1, y2):
        #qp = QPainter()
        #qp.setPen(QPen(Qt.blue, 18))

        x_list = []
        y_list = []
        
        # peak 변수
        baselined_spectrum1 = y1
        baselined_spectrum2 = y2

        # peak값 찾기
        peaks, _ = find_peaks(baselined_spectrum2, height=0, width=2)
        prominences = peak_prominences(baselined_spectrum2, peaks)[0]
        prominence_new = np.percentile(prominences, [0, 25, 50, 75, 80, 100], interpolation='nearest')[4]
        peaks, _ = find_peaks(baselined_spectrum2, prominence=prominence_new)

        # peak 점 표시
        for i in range(len(peaks)):
            x_list.append(x2[peaks[i]])  # x좌표
            y_list.append(baselined_spectrum2[peaks[i]])
        self.graphwidget_3.plot(x_list, y_list, symbol='o', pen=None, symbolSize=10, symbolBrush=('g'))

        
        # peak점 값 출력 (UR2)
        for i in range(len(peaks)):
            x_value = x2[peaks[i]]  # 피크의 x 값
            y_value1 = baselined_spectrum1[peaks[i]]  # 피크의 y 값
            y_value2 = baselined_spectrum2[peaks[i]]  # 피크의 y 값
            change_value = y_value2 - y_value1 # (UR2 - Raw) 차이
            x_value = int(x_value)
            #self.graphwidget_3.plot.text(x_value, y_value2, f'{x_value} \n +{change_value: .2f}', fontsize=10, verticalalignment='bottom')


# table model 만드는 object
class PandasTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(PandasTableModel, self).__init__()
        self.data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            value = self.data.iloc[index.row(), index.column()]
            return str(value)

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.data.columns[section])

            if orientation == Qt.Vertical:
                return str(section + 1)

        return QVariant()
    
    def clear(self):
        # 모델의 데이터를 비우는 메서드
        self.beginResetModel()
        self.data = pd.DataFrame()
        self.endResetModel()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
