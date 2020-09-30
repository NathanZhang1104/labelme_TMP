import cv2
image_cv = cv2.imread(r"C:\Users\Nathan\Documents\books\data\TEM\2\(520-30-180-1)ImageSerial.75.bmp")
print(image_cv)

import sys
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
from PyQt5.QtGui import QPixmap


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)
        lblwidget=QWidget()

        lbl = QLabel(lblwidget)
        pixmap = QPixmap(r"C:\Users\Nathan\Documents\books\data\TEM\2\(520-30-180-1)ImageSerial.75.bmp")  # 按指定路径找到图片，注意路径必须用双引号包围，不能用单引号
        lbl.setPixmap(pixmap)  # 在label上显示图片
        lbl.resize(100, 300)
        lblwidget.resize(200,200)
        lbl.setScaledContents(True)  # 让图片自适应label大小

        hbox.addWidget(lblwidget)

        self.setLayout(hbox)
        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.resize(100, 300)

        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())