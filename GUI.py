import sys
from PyQt5 import (QtWidgets, QtGui, QtCore, Qt)


class MainWindow():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.size = self.app.primaryScreen().size()
        self.width = self.size.width() * 0.8
        self.height = self.size.height() * 0.8

        self.init_GUI()

        self.window.setWindowTitle("Remote Controller")
        self.window.setGeometry(
            50, 50, int(self.width), int(self.height))
        self.window.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.window.show()
        sys.exit(self.app.exec_())

    # create functions to initialize the GUI
    def init_GUI(self):
        stream_width = int(self.width * 0.6)
        stream_height = int(self.height * 0.6)
        terrain_width = int(stream_width * 0.5)
        terrain_height = int(stream_height * 0.5)

        self.stream_video = QtGui.QPixmap("img/044.jpg")
        self.terrain_video = QtGui.QPixmap("img/042.jpg")

        self.label_stream = QtWidgets.QLabel(self.window)
        self.label_stream.setPixmap(self.stream_video)
        self.label_stream.setGeometry(
            10, 10, stream_width, stream_height)

        self.label_terrain = QtWidgets.QLabel(self.window)
        self.label_terrain.setPixmap(self.terrain_video)
        self.label_terrain.setGeometry(
            stream_width + 20, 10, terrain_width, terrain_height)

        # self.createJoystick()

    def createJoystick(self):
        self.btn_up = QtWidgets.QPushButton("", self.window)
        self.btn_up.setIcon(QtGui.QIcon("icon/up-arrow.png"))
        self.btn_up.setIconSize(QtCore.QSize(60, 60))
        self.btn_up.setGeometry(1100, 500, 70, 70)
        self.btn_up.clicked.connect(self.keyPressEvent)

        self.btn_down = QtWidgets.QPushButton("", self.window)
        self.btn_down.setIcon(QtGui.QIcon("icon/down-arrow.png"))
        self.btn_down.setIconSize(QtCore.QSize(60, 60))
        self.btn_down.setGeometry(1100, 700, 70, 70)

        self.btn_left = QtWidgets.QPushButton("", self.window)
        self.btn_left.setIcon(QtGui.QIcon("icon/left-arrow.png"))
        self.btn_left.setIconSize(QtCore.QSize(60, 60))
        self.btn_left.setGeometry(1000, 600, 70, 70)

        self.btn_right = QtWidgets.QPushButton("", self.window)
        self.btn_right.setIcon(QtGui.QIcon("icon/right-arrow.png"))
        self.btn_right.setIconSize(QtCore.QSize(60, 60))
        self.btn_right.setGeometry(1200, 600, 70, 70)

    def full_screen(self):
        pass

    def keyPressEvent(self, event):
        print(event.text)
        if(event.key() == Qt.Key_Up):
            self.send_command("0")
        elif(event.key() == Qt.Key_Down):
            self.send_command("1")
        elif(event.key() == Qt.Key_Left):
            self.send_command("2")
        elif(event.key() == Qt.Key_Right):
            self.send_command("3")
        elif(event.key() == Qt.Key_Space):
            quit()

    def send_command(self, signal):
        print(signal)

    def quit(self):
        QtWidgets.qApp.quit()


if __name__ == "__main__":
    main = MainWindow()
