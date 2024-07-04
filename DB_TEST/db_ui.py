# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:40:16 2023

@author: JSH
"""

from PyQt5.QtWidgets import QFileDialog,QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.figure import Figure

class tt_MainWindow(object):
    def setupUi(self, MainWindow):
        ##MainWindow##
        MainWindow.setFixedSize(1420, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        
        MainWindow.setCentralWidget(self.centralwidget)        
        MainWindow.setWindowTitle("DB_GUI")
        # MainWindow.setWindowIcon(QIcon("./image/Icon.PNG"))
        MainWindow.setStyleSheet('background:#E3F2FD')
        
        self.logo_Label = QtWidgets.QLabel(self.centralwidget)
        self.logo_Label.setGeometry(QtCore.QRect(80, 580, 240, 80))
        logo = QtGui.QPixmap('./image/logo.PNG')
        logo = logo.scaled(240,80)
        self.logo_Label.setPixmap(logo)
        
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(15, 20, 160, 300))
        self.groupBox.setStyleSheet('background:#F5F5F5;' 'border-color:#9E9E9E;' 'border-style:solid;' 'border-width:2px')
        
        self.groupBox3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox3.setGeometry(QtCore.QRect(190, 20, 600, 350))
        self.groupBox3.setStyleSheet('background:#F5F5F5;' 'border-color:#9E9E9E;' 'border-style:solid;' 'border-width:2px')
        
        self.groupBox4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox4.setGeometry(QtCore.QRect(805, 20, 600, 350))
        self.groupBox4.setStyleSheet('background:#F5F5F5;' 'border-color:#9E9E9E;' 'border-style:solid;' 'border-width:2px')
        
        ##GroupBox1##
        self.Server_Label = QtWidgets.QLabel(self.groupBox)
        self.Server_Label.setGeometry(QtCore.QRect(3, 10, 155, 25))
        self.Server_Label.setAlignment(Qt.AlignCenter)
        self.Server_Label.setText("Server Check")
        self.Server_Label.setStyleSheet("border-style:none")
        
        self.Server_status = QtWidgets.QLabel(self.groupBox)
        self.Server_status.setGeometry(QtCore.QRect(3, 35, 155, 25))
        self.Server_status.setAlignment(Qt.AlignCenter)
        self.Server_status.setText("Disconnect")
        self.Server_status.setStyleSheet("border-style:none")
        
        self.Data_Label = QtWidgets.QLabel(self.groupBox)
        self.Data_Label.setGeometry(QtCore.QRect(3, 110, 155, 25))
        self.Data_Label.setAlignment(Qt.AlignCenter)
        self.Data_Label.setText('Data Update')
        self.Data_Label.setStyleSheet('border-color:#BDBDBD;''border-style:none;' 'border-width:1px')
        
        self.Data_Status = QtWidgets.QLabel(self.groupBox)
        self.Data_Status.setGeometry(QtCore.QRect(3, 160, 155, 25))
        self.Data_Status.setAlignment(Qt.AlignCenter)
        self.Data_Status.setText('Need to Update')
        self.Data_Status.setStyleSheet('border-color:#BDBDBD;''border-style:none;' 'border-width:1px')
        
        self.Data_Btn = QtWidgets.QPushButton(self.groupBox)
        self.Data_Btn.setGeometry(QtCore.QRect(30, 260, 110, 25))
        self.Data_Btn.clicked.connect(self.read_db)
        self.Data_Btn.setText("Get Data")
        self.Data_Btn.setStyleSheet("background-color : #F5F5F5")
        
        ##GroupBox3##
        self.Chart1_Label = QtWidgets.QLabel(self.groupBox3)
        self.Chart1_Label.setGeometry(QtCore.QRect(35, 10, 110, 25))
        self.Chart1_Label.setText("Chart 1")
        self.Chart1_Label.setStyleSheet('border-style:none')
        
        self.listWidget = QtWidgets.QListWidget(self.groupBox3)
        self.listWidget.setGeometry(QtCore.QRect(240, 10, 120, 22))
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.addItem("차트표시방법")
        self.listWidget.setStyleSheet('border-color:#BDBDBD;''border-style:solid;' 'border-width:1px')

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.Chart1_CVS = QtWidgets.QVBoxLayout(self.groupBox3)
        self.Chart1_CVS.setGeometry(QtCore.QRect(15, 60, 570, 245))
        self.Chart1_CVS.addWidget(self.canvas)
        
        ##GroupBox4##
        self.Chart2_Label = QtWidgets.QLabel(self.groupBox4)
        self.Chart2_Label.setGeometry(QtCore.QRect(35, 10, 110, 25))
        self.Chart2_Label.setText("Chart 2")
        self.Chart2_Label.setStyleSheet('border-style:none')
        
        self.listWidget = QtWidgets.QListWidget(self.groupBox4)
        self.listWidget.setGeometry(QtCore.QRect(240, 10, 120, 22))
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget.addItem("차트표시방법")
        self.listWidget.setStyleSheet('border-color:#BDBDBD;''border-style:solid;' 'border-width:1px')
        
        self.fig2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.Chart2_CVS = QtWidgets.QVBoxLayout(self.groupBox4)
        self.Chart2_CVS.setGeometry(QtCore.QRect(15, 60, 570, 245))
        self.Chart2_CVS.addWidget(self.canvas2)
        
##클릭 이벤트 발생 가능 라벨##
class Label(QLabel) :
    clicked = pyqtSignal()
    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)

    def mousePressEvent(self, event):
        self.clicked.emit()