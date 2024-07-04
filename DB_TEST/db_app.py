# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 14:42:23 2023

@author: JSH
"""
from PyQt5.QtWidgets import QFileDialog,QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
import re
import os
import pandas as pd
import cv2

import pymysql as ps
import numpy as np
import db_ui as bb

from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import serial
import time

# 아두이노 실시간 스레드
class WorkerThread(QThread):
    # 데이터를 보내기 위한 시그널 정의
    update_data = pyqtSignal(float, float)

    def __init__(self):
        QThread.__init__(self)
        try :
            self.arduino = serial.Serial('COM5', 9600)
        except:
            pass

    def run(self):
        while True:
            y = self.arduino.readline()
            y = y.decode()[:-2]
            y = re.split(" ", y)
            print(y)

            try:
                tmp = float(y[1])
                hum = float(y[3])
                print(tmp, hum)

                # 시그널 발생
                self.update_data.emit(tmp, hum)

            except:
                pass

    def cleanup(self):
        self.arduino.close()

# MYSQL 실시간 Thread(4월 20일)
class WorkerThread2(QThread):
    # 데이터를 보내기 위한 시그널 정의
    update_data2 = pyqtSignal(float, float)

    def __init__(self):
        QThread.__init__(self)
        self.flag = True

    def run(self):
        while self.flag:
            self.con = ps.connect(host = str("211.253.11.217"),
                              port = 11000,
                              user = str("kkamduo"),
                              password = str("ghdwotjr12"),
                              db = str("test"),
                              charset = 'utf8')
            
            data_table = pd.read_sql("select * from 0404test", self.con)
            data_col = tuple(data_table.columns)

            data_fil = []
            # ind = data_table.index
            #시간복잡도 O(N^2)

            for each_col in data_col:
                data_fil.append([each_col,data_table[each_col]])

            try:
                tmp2 = float(list(data_fil[1][1])[-1])
                hum2 = float(list(data_fil[2][1])[-1])
                print(tmp2, hum2)

                # 시그널 발생
                self.update_data2.emit(tmp2, hum2)

            except:
                pass
            time.sleep(1)

    def stop(self):
        self.flag = False
        self.con.close()
        self.quit()
        print("종료")
        self.wait(3000)

class Ui_MainWindow(QtWidgets.QMainWindow,bb.tt_MainWindow): 

    #UI씌우기
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.arduino = serial.Serial('COM5', 9600)

        self.ax = self.fig.add_subplot(111)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_xlim([0,3600])
        self.ax2.set_ylim([0,100])

        self.line, self.line2 = self.ax2.plot(
            np.arange(3600), np.ones(3600, dtype=np.float)*np.nan,
            np.arange(3600), np.ones(3600, dtype=np.float)*np.nan,
            lw=2
        )

        # 쓰레드 생성 및 시작
        self.worker = WorkerThread2()
        self.worker.daemon = True
        self.worker.update_data2.connect(self.update_plot2)  # 시그널 연결
        self.worker.start()

    #Input파일 불러오기
# 
#     def showDialog_1(self):
#         global df
# 
#         try:
#             file_dir = QFileDialog.getExistingDirectory(self.centralwidget, 'Open Data File')
#             
#             test_extension = '.csv'
#             
#             # 차후 시간복잡도 계산후 간단하게 작성가능한 코드로 변경( 현재 O(N^2) )
#             for (root, dirs, files) in os.walk(file_dir):
#                 if len(files) > 0:
#                     for i,file_name in enumerate(files):
#                         if os.path.splitext(file_name)[1] in test_extension:
#                             data_dir = root + '/' + file_name
#                             if i == 0:
#                                 df = pd.read_csv(data_dir,encoding='UTF8')
#                             else :
#                                 cur_df = pd.read_csv(data_dir,encoding='UTF8')
#                                 df = pd.concat([df,cur_df])
# 
#             df = df.drop_duplicates(['관측시간']).sort_values(by='관측시간')
# 
#             time , val = df['관측시간'].values.tolist() , df['예측조위(Cm)'].values.tolist()
# 
#             ax = self.fig.add_subplot(111)
#             
# 
#             # ax = df.plot.bar(x = '관측시간' , y = '예측조위(Cm)',rot = 90)
#             ax.plot(df['관측시간'], df['예측조위(Cm)'])
#             ax.plot(rot=90)
#             test = np.arange(len(df.index))
#             ax.set_xticklabels(time[::1000], rotation = 90)
#             self.canvas.draw()
#             
#             ax2 = self.fig2.add_subplot(111)
#             ax2.bar(df['관측시간'], df['예측조위(Cm)'])
#             ax2.set_xticks(test[::1000])
#             ax2.set_xticklabels(time[::1000], rotation = 90)
#             self.canvas2.draw()
#             # listWidget 추가해서 X,Y축 지정 가능하도록 설계
#             # 그래프 가시화 및 Bar Graph and Marker 추가하기
# 
#         except:
#             QMessageBox.about(self,'Error', 'Check Your Input Data')
# =============================================================================

# MYSQL로부터 데이터 받아들이기    
####### 0412 test code #######
    # 시그널을 수신하여 그래프 업데이트 (시리얼 포트)
    def update_plot(self, tmp, hum):
        old_y = self.line.get_ydata()
        old_y2 = self.line2.get_ydata()
        # print("this is old ", old_y, old_y2)

        new_y = np.r_[old_y[1:], tmp]
        new_y2 = np.r_[old_y2[1:], hum]
        # print("this is new ", new_y, new_y2)

        self.line.set_ydata(new_y)
        self.line2.set_ydata(new_y2)

        self.canvas2.draw()

####### 0420 test code #######
    # MYSQL Real Time 
    def update_plot2(self, tmp2, hum2):
        old_y = self.line.get_ydata()
        old_y2 = self.line2.get_ydata()

        new_y = np.r_[old_y[1:], tmp2]
        new_y2 = np.r_[old_y2[1:], hum2]

        self.line.set_ydata(new_y)
        self.line2.set_ydata(new_y2)

        self.canvas2.draw()

####### 0412 test code #######
    def read_db(self):
        global con

        cur = con.cursor()

        cur.execute("show tables")
        table_list = cur.fetchall()

        data_table = pd.read_sql("select * from 0404test", con)
        data_col = tuple(data_table.columns)

        data_fil = []
        ind = data_table.index
        #시간복잡도 O(N^2)

        for each_col in data_col:
            data_fil.append([each_col,data_table[each_col]])

        # ax = self.fig.add_subplot(111)
        self.ax.plot(ind, data_fil[0][1])
        self.ax.plot(ind, data_fil[1][1])
        self.ax.plot(ind, data_fil[2][1])

        self.canvas.draw()

    def ExportingData(self):
        try:
            cc.Analysis.Export_data(actual_area_pix_num, management_area_pix_num, actual_area_sum, management_area_sum)
        except:
            QMessageBox.about(self,'Error', 'Check Your Data')
    
    def closeEvent(self, event):
        self.worker.stop()
        event.accept()

if __name__ == "__main__":    
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())