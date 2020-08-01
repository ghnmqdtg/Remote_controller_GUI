import sys
import os
import style
import stream
from PyQt5 import (QtWidgets, QtGui, QtCore)


class VLine(QtWidgets.QFrame):
    def __init__(self):
        super(VLine, self).__init__()
        self.setFrameShape(self.VLine)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, url):
        super().__init__()
        self.isStreaming = False
        self.isAnalysing = False
        self.setWindowTitle("Remote Controller")
        self.init_GUI()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    # create functions to initialize the GUI
    def init_GUI(self):
        self.menu_bar()
        # fetch PID
        self.PID = '{:7}'.format(str(os.getpid()))

        self.status_lb_0 = QtWidgets.QLabel("")
        self.status_lb_1 = QtWidgets.QLabel("Stream : Disabled")
        self.status_lb_2 = QtWidgets.QLabel("Terrain : Disabled")
        self.status_lb_0.setFixedWidth(120)
        self.status_lb_1.setFixedWidth(200)
        self.status_lb_2.setFixedWidth(200)

        self.status_lb_0.setText("PID : " + self.PID)
        self.status_btn_1 = QtWidgets.QPushButton("  Start Streaming  ")
        self.status_btn_2 = QtWidgets.QPushButton("  Start Analysing  ")

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

        # add stream videos to labels
        self.status_btn_1.clicked.connect(self.display_stream)
        self.status_btn_2.clicked.connect(self.display_terrain)

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
        self.stream_width = int(self.width * 0.8)
        self.stream_height = int(self.height * 0.8)
        self.terrain_width = int(self.width * 0.3)
        self.terrain_height = int(self.height * 0.3)

        # creat label of camera stream video
        self.label_stream = QtWidgets.QLabel(self)
        self.label_stream.setGeometry(
            20, 45, self.stream_width, self.stream_height)

        # creat label of terrain video
        self.label_terrain = QtWidgets.QLabel(self)
        self.label_terrain.setGeometry(
            self.stream_width + 40, 45, self.terrain_width, self.terrain_height)

        # add status bar
        self.statusBar().showMessage("GUI initializing complete.", 3000)

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

    def display_stream(self):
        if(self.isStreaming is False):
            self.isStreaming = True
            self.status_lb_1.setText("Stream : Enabled ")
            self.status_btn_1.setText("  Stop  Streaming  ")
            self.statusBar().showMessage("RTMP server connecting...", 5000)
            # threads can only be started once
            self.stream_video = stream.StreamVideo(
                url, self.label_stream, self.stream_width, self.stream_height)
            self.stream_video.setDaemon(True)
            self.stream_video.start()
        else:
            self.isStreaming = False
            self.stream_video.stop()
            self.label_stream.setText(" ")
            self.status_lb_1.setText("Stream : Disabled")
            self.status_btn_1.setText("  Start Streaming  ")
            self.statusBar().showMessage("RTMP server disconnected", 2000)

    def display_terrain(self):
        if(self.isAnalysing is False):
            self.isAnalysing = True
            self.status_lb_2.setText("Terrain : Enabled ")
            self.status_btn_2.setText("  Stop  Analysing  ")
            self.statusBar().showMessage("Analysing enabled", 5000)
            # threads can only be started once
            self.terrain_video = stream.StreamVideo(
                url, self.label_terrain, self.terrain_width, self.terrain_height)
            self.terrain_video.setDaemon(True)
            self.terrain_video.start()
        else:
            self.isAnalysing = False
            self.terrain_video.stop()
            self.label_terrain.setText(" ")
            self.status_lb_2.setText("Terrain : Disabled")
            self.status_btn_2.setText("  Start Analysing  ")
            self.statusBar().showMessage("Analysing disabled", 2000)

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
    # url = "rtmp://192.168.43.155/live"
    url = "rtmp://202.69.69.180:443/webcast/bshdlive-pc"

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(url)
    main.show()
    sys.exit(app.exec_())
