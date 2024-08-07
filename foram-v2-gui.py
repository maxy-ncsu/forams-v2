# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.15.9


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QImage

from gui_functions import *
import cv2, imutils, time, serial, os

import numpy as np
import cv2
from Amscope_Camera.camera import *


class WorkerThread(QtCore.QObject):
    update = QtCore.pyqtSignal()

    def __init__(self):
        self.count = 0
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            self.update.emit()
            time.sleep(0.1)

class Ui_Foram_GUI_proto(object):

    def setupUi(self, Foram_GUI_proto):
        # initialize class variables
        self.cam = ToupCamCamera()
        self.cam.open()

        self.cam.set_auto_exposure(False)
        self.exposure = self.cam.get_exposure_time()
        self.cam.set_exposure_time(self.exposure)
        self.gain = self.cam.get_gain()
        self.cam.set_gain(self.gain)
        ports = serial_ports()
        self.arduino = serial.Serial(port=ports[0], baudrate=9600, timeout=.1)
        self.arduino.write(str.encode(str(0)))
        self.trainDetection()
        self.frames = 0
        self.foram_present = True
        time.sleep(2)

        Foram_GUI_proto.setObjectName("Foram_GUI_proto")
        Foram_GUI_proto.resize(800, 850)
        self.centralwidget = QtWidgets.QWidget(Foram_GUI_proto)
        self.centralwidget.setObjectName("centralwidget")


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 790, 595))

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 650, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.changeSolenoid1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(130, 650, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.changeSolenoid2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 650, 93, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.changeSolenoid3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(350, 650, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.changeSolenoid4)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(690, 650, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.saveImg)
        Foram_GUI_proto.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Foram_GUI_proto)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuPrototype = QtWidgets.QMenu(self.menubar)
        self.menuPrototype.setObjectName("menuPrototype")
        Foram_GUI_proto.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Foram_GUI_proto)
        self.statusbar.setObjectName("statusbar")
        Foram_GUI_proto.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuPrototype.menuAction())

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(100, 700, 300, 30))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.exposure * 8)
        self.horizontalSlider.setValue(self.exposure)
        self.horizontalSlider.sliderReleased.connect(self.exposure_changed)
        self.horizontalSlider2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider2.setGeometry(QtCore.QRect(470, 700, 300, 30))
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName("horizontalSlider2")
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(self.gain * 2)
        self.horizontalSlider2.setValue(self.gain)
        self.horizontalSlider2.sliderReleased.connect(self.gain_changed)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 700, 70, 30))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 750, 70, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(100, 750, 70, 30))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(430, 700, 30, 30))
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Foram_GUI_proto)
        QtCore.QMetaObject.connectSlotsByName(Foram_GUI_proto)

        # new
        self.count = 0
        super().__init__()
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.update.connect(self.update)
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start()

        self.solenoid = Solenoids()

    def trainDetection(self):
        '''
        # listing all images in folder

        images = []
        filepath = "./images/12-15-2023/"
        for filename in os.listdir(filepath):
            if filename.endswith("jpg"):
                path = filepath + filename
                images.append(cv2.imread(path))

        # manual positive and negative labeling
        positive = [6, 7, 10, 18, 19, 20, 28, 29]
        negative = list(range(30))
        for i in positive: negative.remove(i)

        # title HOG Parameters
        winSize = (64, 128)
        blockSize = (16, 16)
        blockStride = (8, 8)
        cellSize = (8, 8)
        nbins = 9
        derivAperture = 1
        winSigma = 4.
        histogramNormType = 0
        L2HysThreshold = .2
        gammaCorrection = 0
        nlevels = 64
        self.hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins, derivAperture,
                                winSigma, histogramNormType, L2HysThreshold, gammaCorrection, nlevels)
        self.winStride = (8, 8)
        self.padding = (8, 8)
        self.locations = ((10, 20),)

        hist = self.hog.compute(images[0], self.winStride, self.padding, self.locations)

        # Train SVM
        self.svm = cv2.ml.SVM_create()
        self.svm.setType(cv2.ml.SVM_C_SVC)
        self.svm.setKernel(cv2.ml.SVM_LINEAR)
        self.svm.setC(1)
        #w = np.array([1., 1.])
        #self.svm.setClassWeights(w)

        features = []
        for i in positive: features.append(self.hog.compute(images[i], self.winStride, self.padding, self.locations))
        for i in negative: features.append(self.hog.compute(images[i], self.winStride, self.padding, self.locations))
        features = np.array(features)
        labels = np.append(np.ones(len(positive), dtype=int), -np.ones(len(negative), dtype=int))
        self.svm.train(features, cv2.ml.ROW_SAMPLE, labels)
        '''

    def update(self):
        self.img = np.array(self.cam.get_pil_image())
        frame = cv2.resize(self.img, (780, 585))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap(self.image))

        '''
        if self.frames >= 10:
            self.frames = 0
            results = self.svm.predict(np.array([self.hog.compute(self.img, self.winStride, self.padding, self.locations)]))
            if (results[1][0][0] == 1 and self.foram_present == False):
                print("foram detected")
                self.label_4.setText("Yes")
                self.foram_present = True
            elif (results[1][0][0] == -1 and self.foram_present == True):
                print("no foram detected")
                self.label_4.setText("No")
                self.foram_present = False
        else:
            self.frames += 1
        '''


    def exposure_changed(self):
        self.exposure = self.horizontalSlider.value()
        print("exposure = " + str(self.exposure * 0.001) + " ms")
        self.cam.set_exposure_time(self.exposure)

    def gain_changed(self):
        self.gain = self.horizontalSlider2.value()
        print("gain = " + str(self.gain) + "%")
        self.cam.set_gain(self.gain)

    def retranslateUi(self, Foram_GUI_proto):
        _translate = QtCore.QCoreApplication.translate
        Foram_GUI_proto.setWindowTitle(_translate("Foram_GUI_proto", "MainWindow"))
        self.pushButton.setText(_translate("Foram_GUI_proto", "Solenoid 1"))
        self.pushButton_2.setText(_translate("Foram_GUI_proto", "Solenoid 2"))
        self.pushButton_3.setText(_translate("Foram_GUI_proto", "Solenoid 3"))
        self.pushButton_4.setText(_translate("Foram_GUI_proto", "Solenoid 4"))
        self.pushButton_5.setText(_translate("Foram_GUI_proto", "Save"))
        self.menuPrototype.setTitle(_translate("Foram_GUI_proto", "Prototype"))
        self.label_2.setText(_translate("Foram_GUI_proto", "Exposure"))
        self.label_3.setText(_translate("Foram_GUI_proto", "Detected"))
        self.label_4.setText(_translate("Foram_GUI_proto", "No"))
        self.label_5.setText(_translate("Foram_GUI_proto", "Gain"))

    def changeSolenoid1(self):
        self.solenoid.changeSolenoid(1)
        self.arduino.write(str.encode(str(1)))

    def changeSolenoid2(self):
        self.solenoid.changeSolenoid(2)
        self.arduino.write(str.encode(str(2)))

    def changeSolenoid3(self):
        self.solenoid.changeSolenoid(3)
        self.arduino.write(str.encode(str(3)))

    def changeSolenoid4(self):
        self.solenoid.changeSolenoid(4)
        self.arduino.write(str.encode(str(4)))

    def saveImg(self):
        path = 'images/02-16-2024/image-{:03d}.jpg'.format(self.count)
        self.count += 1
        self.cam.save(path)
        print("image " + str(self.count) + " saved")
        time.sleep(0.1)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Foram_GUI_proto = QtWidgets.QMainWindow()
    ui = Ui_Foram_GUI_proto()
    ui.setupUi(Foram_GUI_proto)
    Foram_GUI_proto.show()
    sys.exit(app.exec_())
