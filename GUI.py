import sys
from PyQt5 import (QtWidgets, QtGui, QtCore, Qt)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.size = QtWidgets.QApplication.primaryScreen().size()
        self.width = self.size.width() * 0.8
        self.height = self.size.height() * 0.8

        self.init_GUI()

        self.setWindowTitle("Remote Controller")
        self.setGeometry(
            50, 50, int(self.width), int(self.height))
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    # create functions to initialize the GUI
    def init_GUI(self):
        stream_width = int(self.width * 0.6)
        stream_height = int(self.height * 0.6)
        terrain_width = int(stream_width * 0.5)
        terrain_height = int(stream_height * 0.5)

        self.stream_video = QtGui.QPixmap("img/044.jpg")
        self.terrain_video = QtGui.QPixmap("img/042.jpg")

        self.label_stream = QtWidgets.QLabel(self)
        self.label_stream.setPixmap(self.stream_video)
        self.label_stream.setGeometry(
            10, 10, stream_width, stream_height)

        self.label_terrain = QtWidgets.QLabel(self)
        self.label_terrain.setPixmap(self.terrain_video)
        self.label_terrain.setGeometry(
            stream_width + 20, 10, terrain_width, terrain_height)

        self.createJoystick()

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
        elif(event.key() == QtCore.Qt.Key_Space):
            self.quit()

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
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
