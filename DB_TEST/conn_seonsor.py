# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:58:14 2023

@author: JSH
"""

import pymysql as ps
from datetime import datetime
import time

if __name__ == "__main__":
    
    con = ps.connect(host = str("127.0.0.1"),
                     user = str("root"),
                     password = str("1234"),
                     db = str("test"),
                     charset = 'utf8')

    cur = con.cursor()
    cur.execute("show tables")
    test = cur.fetchall()

    if "0404test" not in test[0]:
        cur.execute("CREATE TABLE 0404test (time char(255), temp char(255), mor char(255))")
        cur.execute("alter table 0404test convert to character set utf8mb4 collate utf8mb4_unicode_ci")

    sql = 'insert into 0404test (time, temp, mor) values ("%s", "%s", "%s")'

    for i in range(10):
        cur.execute(sql%(str(datetime.now().second), str(i), str(i+10)))
        print(sql%(str(datetime.now().second), str(i), str(i+10)))
        time.sleep(1)

    con.commit()
    
#%% Arduino
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import re

arduino = serial.Serial('COM5', 9600)

fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(0, 100))
line, = ax.plot([], [], lw=2)

max_points = 50
line,line2 = ax.plot(np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, 
                np.arange(max_points), 
                np.ones(max_points, dtype=np.float)*np.nan, 
                lw=2)

def init():
    return line,line2

def animate(i):
    y = arduino.readline()
    y = y.decode()[:-2]
    y = re.split(" ",y)
    tmp = float(y[1])
    hum = float(y[3])

    old_y = line.get_ydata()
    old_y2 = line2.get_ydata()
    print("this is old ", old_y)
    
    new_y = np.r_[old_y[1:], tmp]
    new_y2 = np.r_[old_y2[1:], hum]
    print("this is new ", new_y)
    
    line.set_ydata(new_y)
    line2.set_ydata(new_y2)
    
    return line,line2, new_y,new_y2

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=20, blit=False)

plt.show()

#%% Use Qt Timer(0412)
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create the figure and the canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        # create a timer that will trigger the plot update
        self.timer = QTimer()
        self.timer.setInterval(100)  # update plot every 100ms
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        # initialize the plot
        self.x = np.linspace(0, 2*np.pi, 100)
        self.y = np.sin(self.x)
        self.line, = self.ax.plot(self.x, self.y)

    def update_plot(self):
        # generate new data and update the plot
        self.y = np.sin(self.x + 0.1*np.random.randn())
        self.line.set_ydata(self.y)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    
#%% Use FuncAnimation(0412)
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

import serial
import re
from threading import Thread
import time

class WorkerThread(Thread):
    def __init__(self, fig, canvas):
        Thread.__init__(self)
        self.fig = fig
        self.canvas = canvas
        self.arduino = serial.Serial('COM5',9600)

    def run(self):
        ax = self.fig.add_subplot(111)
        xdata, ydata = [], []
        ax.set_xlim([0,50])
        ax.set_ylim([0,50])
        
        max_points = 50

        self.line,self.line2 = ax.plot(np.arange(max_points), 
                                            np.ones(max_points, dtype=np.float)*np.nan, 
                                            np.arange(max_points), 
                                            np.ones(max_points, dtype=np.float)*np.nan, 
                                            lw=2)

                # create the animation
                # self.anim = FuncAnimation(self.fig, self.update_plot, interval=100)
        print("run")

        def update_plot(i):
            # while True:
                y = self.arduino.readline()
                y = y.decode()[:-2]
                y = re.split(" ",y)
                print(y)

                try : 
                    tmp = float(y[1])
                    hum = float(y[3])
                    print(tmp, hum)

                    old_y = self.line.get_ydata()
                    old_y2 = self.line2.get_ydata()
                    print("this is old ",old_y, old_y2)
                    
                    new_y = np.r_[old_y[1:], tmp]
                    new_y2 = np.r_[old_y2[1:], hum]
                    print("this is new ", new_y,new_y2)

                    self.line.set_ydata(new_y)

                except:
                        pass

                self.canvas.draw()
                time.sleep(0.1)

        self.ani = FuncAnimation(self.fig, update_plot, interval=100)
        self.canvas.draw()
        
    def cleanup(self):
        self.ani.event_source.stop()
        self.arduino.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.setGeometry(100, 100, 640, 480)
        
        # create the figure and the canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        self.worker = WorkerThread(self.fig, self.canvas)
        self.worker.start()
        
    def closeEvent(self, event):
        self.worker.cleanup()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    
#%%

        # initialize the plot
# =============================================================================
#         self.x = np.linspace(0, 2*np.pi, 100)
#         self.y = np.sin(self.x)
#         self.line, = self.ax.plot([], [],lw = 2)
# =============================================================================


# =============================================================================
#         max_points = 50
#         self.line,self.line2 = self.ax.plot(np.arange(max_points), 
#                         np.ones(max_points, dtype=np.float)*np.nan, 
#                         np.arange(max_points), 
#                         np.ones(max_points, dtype=np.float)*np.nan, 
#                         lw=2)
# 
#         # create the animation
#         self.anim = FuncAnimation(self.fig, self.update_plot, interval=100)
# =============================================================================
# =============================================================================
#     def update_plot(self, i):
#         # generate new data and update the plot
# # =============================================================================
# #         self.y = np.sin(self.x + i/10)
# #         self.line.set_ydata(self.y)
# # =============================================================================
#         y = self.arduino.readline()
#         y = y.decode()[:-2]
#         y = re.split(" ",y)
#         
# 
#         try : 
#             tmp = float(y[1])
#             hum = float(y[3])
#     
#             print(tmp, hum)
#             
#             old_y = self.line.get_ydata()
#             old_y2 = self.line2.get_ydata()
# 
#             print("this is old ",old_y, old_y2)
#             
#             new_y = np.r_[old_y[1:], tmp]
#             new_y2 = np.r_[old_y2[1:], hum]
#             
#             print("this is new ", new_y,new_y2)
#             
#             self.line.set_ydata(new_y)
#             # self.line2.set_ydata(new_y2)
#             
#             # return self.line, self.line2
#             # self.ax2.relim()
#             # self.ax2.autoscale_view()
#             
#             # self.canvas2.draw()
#         except:
#                 pass
# =============================================================================

#%%
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, pyqtSignal, QThread
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation

import serial
import re
from threading import Thread


class WorkerThread(QThread):
    # 데이터를 보내기 위한 시그널 정의
    update_data = pyqtSignal(float, float)

    def __init__(self):
        QThread.__init__(self)
        self.arduino = serial.Serial('COM5', 9600)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # create the figure and the canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        # 그래프 초기화
        self.line, self.line2 = self.ax.plot(
            np.arange(50), np.ones(50, dtype=np.float)*np.nan,
            np.arange(50), np.ones(50, dtype=np.float)*np.nan,
            lw=2
        )
        self.ax.set_xlim([0, 50])
        self.ax.set_ylim([0, 50])

        # 쓰레드 생성 및 시작
        self.worker = WorkerThread()
        self.worker.update_data.connect(self.update_plot)  # 시그널 연결
        self.worker.start()

    # 시그널을 수신하여 그래프 업데이트
    def update_plot(self, tmp, hum):
        old_y = self.line.get_ydata()
        old_y2 = self.line2.get_ydata()
        # print("this is old ", old_y, old_y2)

        new_y = np.r_[old_y[1:], tmp]
        new_y2 = np.r_[old_y2[1:], hum]
        # print("this is new ", new_y, new_y2)

        self.line.set_ydata(new_y)
        self.line2.set_ydata(new_y2)

        self.canvas.draw()

    def closeEvent(self, event):
        self.worker.cleanup()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

#%%
import pymysql as ps
import pandas as pd

con = ps.connect(host = str("211.253.11.217"),
                 port = 11000,
                 user = str("kkamduo"),
                 password = str("ghdwotjr12"),
                 db = str("test"),
                 charset = 'utf8')
cur = con.cursor()

cur.execute("show tables")
table_list = cur.fetchall()

data_table = pd.read_sql("select * from 0404test", con)
data_col = tuple(data_table.columns)

data_fil = []
ind = data_table.index

for each_col in data_col:
    data_fil.append([each_col,data_table[each_col]])