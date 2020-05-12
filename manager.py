import sys
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMenu, QAction, qApp, QSystemTrayIcon, QStyle
from PyQt5 import uic
from qt.qt_func import resource_path
from data import db_session
from data.users import User


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.Window)
        if __name__ == '__main__':
            uic.loadUi(resource_path('qt\\main_qt.ui'), self)
        else:
            uic.loadUi(resource_path('qt\\main_qt.ui'), self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin panel')
        # ----------------- List_user -----------------
        db_session.global_init("db/catclient.sqlite")
        session = db_session.create_session()
        users = session.query(User).all()
        del users[0]
        list_name_user = [i.name for i in users]
        self.list_user.addItems(list_name_user)
        self.bselect_user.clicked.connect(self.select_user)
        # ----------------- List_dirs -----------------
        self.bselect_dir.clicked.connect(self.select_dir)

    def select_user(self):
        user = self.list_user.currentText()
        session = db_session.create_session()
        users = session.query(User).filter(User.name == user).first()
        if users:
            print(users.dirs)
            if users.dirs is None:
                self.list_dirs.addItems('Not found')
            else:
                print(users.dirs)
                dirs = users.dirs.split(',')
                self.list_dirs.addItems(dirs)


    def select_dir(self):
        None


def server():
    print("Starting up the server")
    try:
        import production_run
    except Exception as e:
        return 'cant find the production release file'
    try:
        production_run.run()
    except Exception as e:
        return 'server crashed. stack:' + str(e)
    print("server shut down")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.main_app = Main()
        self.move(180, 100)
        self.setFixedSize(400, 300)
        self.setWindowTitle('control')

        self.server = threading.Thread(target=server)

        self.toclose = False
        self.all_buttons = []

        self.start_button = QPushButton('start/stop', parent=self)
        self.start_button.setGeometry(100, 100, 200, 100)
        self.start_button.action = 'start'
        self.all_buttons.append(self.start_button)

        for i in self.all_buttons:
            i.clicked.connect(self.onClick)

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def onClick(self):
        btn = self.sender().action
        print(btn, 'action released!')
        if btn == 'start':
            if not self.server.is_alive():
                self.main_app.show()

                self.server.start()
                self.start_button.setEnabled(0)
                self.start_button.setText('server running')

    def closeEvent(self, evnt):
        if self.toclose:
            super(App, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()


app_style = QtWidgets.QApplication(sys.argv)
file = QFile(":/dark.qss")
file.open(QFile.ReadOnly | QFile.Text)
stream = QTextStream(file)
app_style.setStyleSheet(stream.readAll())

app = QApplication(sys.argv)
form = App()
form.show()
sys.exit(app.exec())
