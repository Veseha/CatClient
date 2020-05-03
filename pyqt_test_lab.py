from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication
import breeze_resources
import threading
from _ast import While



class Communicate(QObject):
       signal = pyqtSignal(int, str)

class My_Gui(QWidget):
       def __init__(self):
           super().__init__()

           self.comm = Communicate()
           self.comm.signal.connect(self.append_data)
           self.initUI()

       def initUI(self):

           btn_count = QPushButton('Count')
           btn_count.clicked.connect(self.start_counting)
           self.te = QTextEdit()

           vbox = QVBoxLayout()
           vbox.addWidget(btn_count)
           vbox.addWidget(self.te)

           self.setLayout(vbox)
           self.setWindowTitle('MultiThreading in PyQT5')
           self.setGeometry(400, 400, 400, 400)
           self.show()

       def count(self, comm):
           '''
           for i in range(10):
               data = "Data "+str(i)
               comm.signal.emit(i, data)
           '''
           i = 0
           while i < 101:
               data = "Data "+str(i)
               comm.signal.emit(i, data)
               i+=1

       def start_counting(self):
           my_Thread = threading.Thread(target=self.count, args=(self.comm,))
           my_Thread.start()

       def append_data(self, num, data):
           self.te.append(str(num) + " " + data)

if __name__ == '__main__':
       app = QApplication(sys.argv)
       my_gui = My_Gui()
       sys.exit(app.exec_())

       app = QApplication(sys.argv)
       file = QFile(":/dark.qss")
       file.open(QFile.ReadOnly | QFile.Text)
       stream = QTextStream(file)
       app.setStyleSheet(stream.readAll())