#!/bin/python3
import cv2
from deepface import DeepFace
from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageQt
import numpy as np
import sys, random
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout, QVBoxLayout)
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter

total={
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0
}
total_avg={
    'angry': 0,
    'disgust': 0,
    'fear': 0,
    'happy': 0,
    'sad': 0,
    'surprise': 0,
    'neutral': 0
}
num_songs = 0


class Worker(QObject):
    finished = pyqtSignal()  # give worker class a finished signal
    imgvalsig = pyqtSignal(np.ndarray, str, float, int)
    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True
    def print_status(self, stats):
        val = f"Current Frame Status: Primary: {str(stats[0]['dominant_emotion'])}\n"
        for emot in stats[0]['emotion']:
            val += f"{emot}: {str(stats[0]['emotion'][emot])}\n"
        print(val, end="")
        print('---------------------------------------------')

    def next_song(self, s_total):
        num_songs += 1

        for elem in s_total.keys():
            total[elem] += s_total[elem]
        
        for elem in total_avg.keys():
            total_avg[elem] = total[elem] / num_songs

    def calc_diff(self, s_total_avg):
        return total_avg['happy'] - s_total_avg['happy']

    def do_work(self):
        print("RUNNING")
        song_total={
            'angry': 0,
            'disgust': 0,
            'fear': 0,
            'happy': 0,
            'sad': 0,
            'surprise': 0,
            'neutral': 0
        }

        song_avg={
            'angry': 0,
            'disgust': 0,
            'fear': 0,
            'happy': 0,
            'sad': 0,
            'surprise': 0,
            'neutral': 0
        }

        song_frame_num = 0

        while self.continue_run:
            # Create a VideoCapture object to access the webcam
            cap = cv2.VideoCapture(0)
            # Check if the webcam is opened successfully
            if not cap.isOpened():
                print("Cannot access the webcam")
                exit()
            # Read a frame from the webcam
            ret, frame = cap.read()
            # Check if the frame is successfully read
            if not ret:
                print("Cannot capture a frame")
                exit()
            # Release the VideoCapture object and close all windows
            cap.release()
            cv2.destroyAllWindows()
            # read image
            img=frame
            # storing the result
            result = DeepFace.analyze(img,actions=['emotion'])

            self.print_status(result)
            song_frame_num += 1
            for emot in result[0]['emotion']:
                song_total[emot] += result[0]['emotion'][emot]
                song_avg[emot] = song_total[emot]/song_frame_num

            hapDifferential = self.calc_diff(song_avg)
            self.imgvalsig.emit(img, result[0]['dominant_emotion'], hapDifferential, song_frame_num)  # emit the finished signal when the loop is done
            if song_frame_num > 5 and hapDifferential < -0.1:
                print("Change song")
            print(song_avg)
            print(song_total)
    def stop(self):
        self.continue_run = False  # set the run condition to false on stop

class Gui(QWidget):
    stop_signal = pyqtSignal()  # make a stop signal to communicate with the worker in another thread
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # Buttons:
        self.btn_start = QPushButton('Start')
        self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(50, 50)
        self.btn_stop = QPushButton('Stop')
        self.btn_stop.resize(self.btn_stop.sizeHint())
        self.btn_stop.move(150, 50)
        # General setup
        # self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('ThreadTest')
        self.layout = QGridLayout()
        self.layout.addWidget(self.btn_start, 0, 0)
        self.layout.addWidget(self.btn_stop, 0, 1)
        self.setLayout(self.layout)

        # generate data
        table = np.zeros((256,256,3), dtype=np.uint8)
        # for x in table:
        #     for y in x:
        #         y = (255,255,255)
        # for i in range(256):
        #     table[:,i,0] = i
        #     table[i,:,1] = i
        # table[:,:,2] = (2*255 - table[:,:,0] - table[:,:,1]) // 2
        # convert data to QImage using PIL
        img = Image.fromarray(table, mode='RGB')
        qt_img = ImageQt.ImageQt(img)

        self.textDataLayout = QVBoxLayout()
        self.imgWidget = QtWidgets.QLabel()
        self.imgWidget.setPixmap(QtGui.QPixmap.fromImage(qt_img))
        self.textDataLayout.addWidget(self.imgWidget)
        self.primaryEmotWidget = QtWidgets.QLabel("")
        self.textDataLayout.addWidget(self.primaryEmotWidget)
        self.hapDiffWidget = QtWidgets.QLabel("")
        self.textDataLayout.addWidget(self.hapDiffWidget)


        set0 = QBarSet('Song Avg')
        set1 = QBarSet('Total Avg')

        set0.append([random.randint(0, 10) for i in range(7)])
        set1.append([random.randint(0, 10) for i in range(7)])

        series = QBarSeries()
        series.append(set0)
        series.append(set1)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Emotion Confidence Values')
        emotions = ('angry','disgust','fear','happy','sad','surprise','neutral')
        axisX = QBarCategoryAxis()
        axisX.append(emotions)
        axisY = QValueAxis()
        # axisY.setRange(0, 15)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        chartView = QChartView(chart)
        # self.setCentralWidget(chartView)
        self.textDataLayout.addWidget(chartView)


        self.textDataDisplays = QWidget()
        self.textDataDisplays.setLayout(self.textDataLayout)
        self.layout.addWidget(self.textDataDisplays, 1, 0)
        # Thread:
        self.thread = QThread()
        self.worker = Worker()
        self.stop_signal.connect(self.worker.stop)  # connect stop signal to worker stop method
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.on_data_ready)
        self.worker.imgvalsig.connect(self.updateImgVal)

        self.thread.started.connect(self.worker.do_work)
        self.thread.finished.connect(self.worker.stop)

        # Start Button action:
        self.btn_start.clicked.connect(self.thread.start)

        # Stop Button action:
        self.btn_stop.clicked.connect(self.stop_thread)

        self.show()
    def updateImgVal(self, data, primaryEmot, hapDiff, frNum):
        print("Emit running")
        img = Image.fromarray(data, mode='RGB')
        qt_img = ImageQt.ImageQt(img)
        self.imgWidget.setPixmap(QtGui.QPixmap.fromImage(qt_img))
        self.primaryEmotWidget.setText(f"Primary emotion: {primaryEmot}")
        self.hapDiffWidget.setText(f"Frame: {frNum} Happiness differential: {hapDiff}")
    def on_data_ready(self, data):
        print(data)

    # When stop_btn is clicked this runs. Terminates the worker and the thread.
    def stop_thread(self):
        print("stopping and exiting")
        self.btn_stop.setText("Stopped")
        self.stop_signal.emit()  # emit the finished signal on stop
        # sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())

