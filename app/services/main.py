#!/bin/python3
import cv2
from deepface import DeepFace
from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageQt
import numpy as np
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout)
from PyQt5.QtCore import QThread, QObject, pyqtSignal

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
    imgvalsig = pyqtSignal(np.ndarray)
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
            self.imgvalsig.emit(img)  # emit the finished signal when the loop is done
            # storing the result
            result = DeepFace.analyze(img,actions=['emotion'])

            self.print_status(result)
            song_frame_num += 1
            for emot in result[0]['emotion']:
                song_total[emot] += result[0]['emotion'][emot]
                song_avg[emot] = song_total[emot]/song_frame_num

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
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('ThreadTest')
        self.layout = QGridLayout()
        self.layout.addWidget(self.btn_start, 0, 0)
        self.layout.addWidget(self.btn_stop, 0, 1)
        self.setLayout(self.layout)

        # generate data
        table = np.zeros((256,256,3), dtype=np.uint8)
        # convert data to QImage using PIL
        img = Image.fromarray(table, mode='RGB')
        qt_img = ImageQt.ImageQt(img)
        self.imgWidget = QtWidgets.QLabel()
        self.imgWidget.setPixmap(QtGui.QPixmap.fromImage(qt_img))
        self.layout.addWidget(self.imgWidget, 1, 0)
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
    def updateImgVal(self, data):
        print("Emit running")
        img = Image.fromarray(data, mode='RGB')
        qt_img = ImageQt.ImageQt(img)
        self.imgWidget.setPixmap(QtGui.QPixmap.fromImage(qt_img))
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

