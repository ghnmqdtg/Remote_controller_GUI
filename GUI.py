import sys
import os
from threading import Thread
from PyQt5 import (QtWidgets, QtGui, QtCore)
from stream import StreamVideo


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, url):
        super().__init__()

        # set window size
        self.size = QtWidgets.QApplication.primaryScreen().size()
        self.width = self.size.width() * 0.8
        self.height = self.size.height() * 0.8

        self.stylesheet = self.style()

        self.init_GUI()

        self.setWindowTitle("Remote Controller")
        self.setStyleSheet(self.stylesheet)
        self.setGeometry(
            50, 50, int(self.width), int(self.height))
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    # create functions to initialize the GUI
    def init_GUI(self):
        self.font = QtGui.QFont('Helvetica', 20, QtGui.QFont.Bold)
        self.menu_bar()
        stream_width = int(self.width * 0.6)
        stream_height = int(self.height * 0.6)
        terrain_width = int(stream_width * 0.5)
        terrain_height = int(stream_height * 0.5)

        # creat label of camera stream video
        self.label_stream = QtWidgets.QLabel(self)
        self.label_stream.setGeometry(
            10, 35, stream_width, stream_height)

        # creat label of terrain video
        self.label_terrain = QtWidgets.QLabel(self)
        self.label_terrain.setGeometry(
            stream_width + 20, 35, terrain_width, terrain_height)

        # add status bar
        self.statusBar().showMessage("GUI initializing complete.")

        # comment out for adding new functions

        # add stream videos to labels
        self.stream_video = self.display(
            self.label_stream, stream_width, stream_height)

        self.terrain_video = self.display(
            self.label_terrain, terrain_width, terrain_height)

        # add joystick to MainWindow
        self.createJoystick()

    # add menu bar to MainWindow
    def menu_bar(self):
        # create menu bar
        menuBar = self.menuBar()

        # create the action
        quitAction = QtWidgets.QAction("Quit", self)
        quitAction.setShortcut("CTRL+Q")

        # add action to menu
        controlMenu = menuBar.addMenu("&Control")
        controlMenu.addAction(quitAction)

        quitAction.triggered.connect(self.quit)

    def display(self, out_label, width, height):
        self.PID = str(os.getpid())
        self.statusBar().showMessage("PID : " + self.PID)

        # print("PID:", os.getpid())  # for testing
        Thread(
            target=StreamVideo(url, out_label, width, height).output).start()

    def createJoystick(self):
        self.btn_up = QtWidgets.QPushButton("", self)
        self.btn_up.setIcon(QtGui.QIcon("icon/up-arrow.png"))
        self.btn_up.setIconSize(QtCore.QSize(60, 60))
        self.btn_up.setGeometry(1100, 500, 70, 70)
        # self.btn_up.clicked.connect(self.send_command)

        self.btn_down = QtWidgets.QPushButton("", self)
        self.btn_down.setIcon(QtGui.QIcon("icon/down-arrow.png"))
        self.btn_down.setIconSize(QtCore.QSize(60, 60))
        self.btn_down.setGeometry(1100, 700, 70, 70)

        self.btn_left = QtWidgets.QPushButton("", self)
        self.btn_left.setIcon(QtGui.QIcon("icon/left-arrow.png"))
        self.btn_left.setIconSize(QtCore.QSize(60, 60))
        self.btn_left.setGeometry(1000, 600, 70, 70)

        self.btn_right = QtWidgets.QPushButton("", self)
        self.btn_right.setIcon(QtGui.QIcon("icon/right-arrow.png"))
        self.btn_right.setIconSize(QtCore.QSize(60, 60))
        self.btn_right.setGeometry(1200, 600, 70, 70)

    def keyPressEvent(self, event):
        # print(event.text())
        if(event.key() == QtCore.Qt.Key_Up):
            self.send_command("0")
        elif(event.key() == QtCore.Qt.Key_Down):
            self.send_command("1")
        elif(event.key() == QtCore.Qt.Key_Left):
            self.send_command("2")
        elif(event.key() == QtCore.Qt.Key_Right):
            self.send_command("3")
        elif(event.key() == QtCore.Qt.Key_F11):
            self.full_screen()

    def send_command(self, signal):
        print(signal)

    def style(self):
        stylesheet = """
            QMenuBar {
                background-color: #2e2e2e;
                color: #e0e0e0;
                font: bold;
                font-size: 16px;
                font-family: Helvetica;
            }

            QMenuBar::item {
                background-color: transparent;
            }

            QMenuBar::item:selected {
                background-color: #ffffff;
                color: #2e2e2e;
            }

            QMenu {
                background-color: #2e2e2e;
                color: #ffffff;
                font: bold;
                font-size: 16px;
                font-family: Helvetica;
            }

            QMenu::item:selected {
                background-color: #ffffff;
                color: #2e2e2e;
            }
        """

        return stylesheet

    def full_screen(self):
        if(self.windowState() & QtCore.Qt.WindowFullScreen):
            self.showNormal()
        else:
            self.showFullScreen()

    def quit(self):
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    # RTMP URL of camera stream video
    url = "rtmp://202.69.69.180:443/webcast/bshdlive-pc"

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(url)
    main.show()
    sys.exit(app.exec_())
