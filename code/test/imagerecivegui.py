import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap,QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
import time
import servervid


#class Sv(QThread):
#    def run():
#        servervid.start()


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.title = "Image Reciever"
        self.setWindowTitle(self.title)
        self.label = QLabel(self)
        self.setCentralWidget(self.label)
        self.resize(500,750)
        #Start Qtimer
        timer = QTimer(self)
        timer.timeout.connect(self.refr)
        timer.start(1000)
        #starting server thread
        #self.server = Sv()
        #self.server.start()

    def refr(self):
        #recieves from server if possible
        #a = servervid.recimage
        if a:
            b = (255 << 24 | a[:,:,0] << 16 | a[:,:,1] << 8 | a[:,:,2]).flatten() # pack RGB values
            im = QImage(b, a.shape[0], a.shape[1], QImage.Format_ARGB32)
            self.label.setPixmap(QPixmap(im))
        self.update()


app = QApplication(sys.argv)
w = MainWindow()
w.show()

sys.exit(app.exec_())
