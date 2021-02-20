import sys
import threading
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import time

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.pixmaps = [QPixmap('cat.jpg'),QPixmap('dog.jpg')]
        self.title = "Image Viewer"
        self.setWindowTitle(self.title)
        self.label = QLabel(self)
        pixmap = self.pixmaps[0]
        self.pixi = 0
        self.label.setPixmap(pixmap)
        self.setCentralWidget(self.label)
        self.resize(pixmap.width(), pixmap.height())
        timer = QTimer(self)
        timer.timeout.connect(self.refr)
        timer.start(1000)
    def refr(self):
        if self.pixi:
            self.pixi = 0
        else:
            self.pixi = 1
        pixmap = self.pixmaps[self.pixi]
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        self.update()

app = QApplication(sys.argv)
w = MainWindow()
w.show()

sys.exit(app.exec_())
