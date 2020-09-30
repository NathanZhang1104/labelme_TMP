# class ThreWight():
#

# ! /usr/bin/python3
# coding = utf-8
# from PyQt5 import QtGui,QtCore,Qt
import sys
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRect, QMetaObject, QCoreApplication, pyqtSlot, QPropertyAnimation, \
    QThread
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication,QLabel,\
    QWidget,QHBoxLayout,QPushButton
import numpy as np
import cv2
# from gevent.libev.corecext import SIGNAL, time
from PyQt5 import QtCore
import time
import numpy
from labelme.shape import Shape

def cvImgtoQtImg(cv_img):  # 定义opencv图像转PyQt图像的函数
    cv2.imwrite("./test.png",cv_img)
    qimg=QImage("./test.png")
    return qimg

def get_hull_fromimg(img,K,offset):
    '''
    通过kmeans聚类，以及一些二值化处理，提取图片中的目标区域。
    '''

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    Z = gray_img.reshape((-1,1))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0)

    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    quant_img = res.reshape((gray_img.shape))
    thre,bin_img=cv2.threshold(gray_img,int(min(center.reshape((-1,1)))),255,cv2.THRESH_BINARY_INV)
    bin_img=cv2.erode(bin_img, None, iterations=1)
    bin_img=cv2.dilate(bin_img, None, iterations=4)

    contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE,offset=offset)
    shapes_list=[]
    for contour in contours:
        if((cv2.arcLength(contour,False)<50 and len(contours)>1)
                or cv2.arcLength(contour,False)>1000):continue

        hull=cv2.convexHull(contour, False)
        cur_shape=Shape(shape_type="polygon")
        for point in hull:
            cur_shape.addPoint(QtCore.QPoint(point[0][0],point[0][1]))
        cur_shape.addPoint(QtCore.QPoint(hull[0][0][0], hull[0][0][1]))
        shapes_list.append(cur_shape)

    return  shapes_list,quant_img

# def thre(img):


class ThreWight(QWidget):
    def __init__(self):
        super(ThreWight, self).__init__()
        # self.setupUi(self)
        hbox = QHBoxLayout(self)
        lblwidget = QWidget()
        self.lbl = QLabel(lblwidget)
        # self.setpixmap(image_cv)

        self.lbl.resize(400, 400)
        lblwidget.resize(400, 400)

        hbox.addWidget(lblwidget)

        self.setLayout(hbox)
        self.setWindowTitle('Red Rock')
        self.resize(400, 400)

        self.show()

        # self.showCamer()

    def setpixmap(self,qimg=None):

        pixmap01 = QPixmap.fromImage(qimg)
        self.lbl.setPixmap(pixmap01)  # 在label上显示图片
        self.lbl.setScaledContents(True)  # 让图片自适应label大小

        pass

if __name__ == "__main__":
    cvimg = cv2.imread(r"C:\Users\Nathan\Documents\books\data\TEM\2\(520-30-180-1)ImageSerial.75.bmp")
    qimg = cvImgtoQtImg(cvimg)
    app = QApplication(sys.argv)
    myshow = ThreWight()
    myshow.setpixmap(qimg)
    myshow.show()
    sys.exit(app.exec_())
