import sys
import os
import style
from threading import Thread
from PyQt5 import (QtWidgets, QtGui, QtCore)
from stream import StreamVideo


class VLine(QtWidgets.QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Remote Controller")
        self.init_GUI()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    # create functions to initialize the GUI
    def init_GUI(self):
        self.menu_bar()
        self.PID = '{:7}'.format(str(os.getpid()))

        self.status_lb_0 = QtWidgets.QLabel("")
        self.status_lb_1 = QtWidgets.QLabel("Stream : Running")
        self.status_lb_2 = QtWidgets.QLabel("Terrain: Running")

        self.status_lb_0.setText("PID : " + self.PID)
        self.status_btn_1 = QtWidgets.QPushButton("  Start Streaming  ")
        self.status_btn_2 = QtWidgets.QPushButton("  Start Analysis   ")

        self.status_lb_0.setObjectName("status_lb")
        self.status_lb_1.setObjectName("status_lb")
        self.status_lb_2.setObjectName("status_lb")
        self.status_btn_1.setObjectName("status_btn")
        self.status_btn_2.setObjectName("status_btn")

        self.statusBar().addPermanentWidget(self.status_lb_0)
        self.statusBar().addPermanentWidget(self.status_lb_1)
        self.statusBar().addPermanentWidget(self.status_lb_2)
        self.statusBar().addPermanentWidget(self.status_btn_1)
        self.statusBar().addPermanentWidget(self.status_btn_2)

        # button clicked
        self.status_btn_1.clicked.connect(
            lambda: self.statusBar().showMessage("RTMP Server Conneting..."))

        self.status_btn_2.clicked.connect(
            lambda: self.statusBar().showMessage("Initializing Analysis..."))

        # set style
        self.style_main = style.style_main(self)
        self.style_statusbar = style.style_statusbar(self)
        self.setStyleSheet(self.style_main)
        self.statusBar().setStyleSheet(self.style_statusbar)

        # set window size
        self.size = QtWidgets.QApplication.primaryScreen().size()
        self.width = self.size.width() * 0.8
        self.height = self.size.height() * 0.8
        self.setGeometry(
            50, 50, int(self.width), int(self.height))
        stream_width = int(self.width * 0.8)
        stream_height = int(self.height * 0.8)
        terrain_width = int(self.width * 0.3)
        terrain_height = int(self.height * 0.3)

        # creat label of camera stream video
        self.label_stream = QtWidgets.QLabel(self)
        self.label_stream.setGeometry(
            20, 45, stream_width, stream_height)

        # creat label of terrain video
        self.label_terrain = QtWidgets.QLabel(self)
        self.label_terrain.setGeometry(
            stream_width + 40, 45, terrain_width, terrain_height)

        # add status bar
        self.statusBar().showMessage("GUI initializing complete.", 3000)

        # comment out for adding new functions
        # add stream videos to labels
        # set as daemon thread
        # so that it can be killed when main thread is closed
        self.stream_video = Thread(
            target=StreamVideo(url, self.label_stream, stream_width, stream_height).output, daemon=True)
        self.stream_video.start()

        self.terrain_video = Thread(
            target=StreamVideo(url, self.label_terrain, terrain_width, terrain_height).output, daemon=True)
        self.terrain_video.start()

        # add joystick to MainWindow

        # self.createJoystick()

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
        print("PID:", os.getpid())  # for testing

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
            self.statusBar().showMessage("Up")
            self.send_command("0")
        elif(event.key() == QtCore.Qt.Key_Down):
            self.statusBar().showMessage("Down")
            self.send_command("1")
        elif(event.key() == QtCore.Qt.Key_Left):
            self.statusBar().showMessage("Left")
            self.send_command("2")
        elif(event.key() == QtCore.Qt.Key_Right):
            self.statusBar().showMessage("Right")
            self.send_command("3")
        elif(event.key() == QtCore.Qt.Key_F11):
            self.full_screen()

    def send_command(self, signal):
        print(signal)

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
