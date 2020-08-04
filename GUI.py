import sys
import os
import style
import stream
import requests
from PyQt5 import (QtWidgets, QtGui, QtCore, Qt)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.isStreaming = False
        self.isAnalysing = False
        self.isControlling = False
        self.setWindowTitle("Remote Controller")
        self.url_stream = ""
        self.url_terrain = ""
        self.url_control = ""
        self.init_GUI()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    # create functions to initialize the GUI
    def init_GUI(self):
        self.menu_bar()
        # fetch PID
        self.PID = '{:7}'.format(str(os.getpid()))

        # status bar initializing
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
        # self.status_btn_1.setObjectName("status_btn")
        # self.status_btn_2.setObjectName("status_btn")

        self.statusBar().addPermanentWidget(self.status_lb_0)
        self.statusBar().addPermanentWidget(self.status_lb_1)
        self.statusBar().addPermanentWidget(self.status_lb_2)
        self.statusBar().addPermanentWidget(self.status_btn_1)
        self.statusBar().addPermanentWidget(self.status_btn_2)

        self.statusBar().showMessage("GUI initializing complete.", 3000)

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
            50, 50, 1268, 772)
        self.stream_width = int(self.width * 0.8)
        self.stream_height = int(self.height * 0.8)
        self.terrain_width = int(self.width * 0.3)
        self.terrain_height = int(self.height * 0.3)

        # creat label of camera stream video
        self.label_stream = QtWidgets.QLabel(self)
        self.label_stream.setGeometry(
            20, 45, self.stream_width, self.stream_height)
        self.label_stream.setAlignment(QtCore.Qt.AlignCenter)
        self.label_stream.setObjectName("video")

        # creat label of terrain video
        self.label_terrain = QtWidgets.QLabel(self)
        self.label_terrain.setGeometry(
            self.stream_width + 40, 45, self.terrain_width, self.terrain_height)
        self.label_terrain.setAlignment(QtCore.Qt.AlignCenter)
        self.label_terrain.setObjectName("video")

        # URL entering box
        self.url_lb_1 = QtWidgets.QLabel("RTMP Server URL", self)
        self.url_lb_1.setGeometry(30, self.stream_height + 90, 150, 30)
        self.textEdit_url_1 = QtWidgets.QTextEdit(self)
        self.textEdit_url_1.setGeometry(200, self.stream_height + 90, 780, 30)
        self.text_btn_url_1 = QtWidgets.QPushButton("Submit", self)
        self.text_btn_url_1.setGeometry(1000, self.stream_height + 90, 100, 30)
        self.text_btn_url_1.clicked.connect(self.URL_read)

        self.url_lb_2 = QtWidgets.QLabel("Terrain data source", self)
        self.url_lb_2.setGeometry(30, self.stream_height + 150, 200, 30)
        self.textEdit_url_2 = QtWidgets.QTextEdit(self)
        self.textEdit_url_2.setGeometry(240, self.stream_height + 150, 740, 30)
        self.text_btn_url_2 = QtWidgets.QPushButton("Submit", self)
        self.text_btn_url_2.setGeometry(1000, self.stream_height + 150, 100, 30)
        self.text_btn_url_2.clicked.connect(self.URL_read)

        self.url_lb_3 = QtWidgets.QLabel("Backend Server", self)
        self.url_lb_3.setGeometry(30, self.stream_height + 210, 200, 30)
        self.textEdit_url_3 = QtWidgets.QTextEdit(self)
        self.textEdit_url_3.setGeometry(200, self.stream_height + 210, 780, 30)
        self.text_btn_url_3 = QtWidgets.QPushButton("Submit", self)
        self.text_btn_url_3.setGeometry(1000, self.stream_height + 210, 100, 30)
        self.text_btn_url_3.clicked.connect(self.backend_connection)

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
        if(self.url_stream != ""):
            if(self.isStreaming is False):
                self.isStreaming = True
                self.textEdit_url_1.setReadOnly(True)
                self.text_btn_url_1.setEnabled(False)
                self.status_lb_1.setText("Stream : Enabled ")
                self.status_btn_1.setText("  Stop  Streaming  ")
                self.statusBar().showMessage("RTMP server connecting...", 5000)
                # threads can only be started once
                self.stream_video = stream.StreamVideo(
                    self.url_stream, self.label_stream, self.stream_width, self.stream_height)
                self.stream_video.setDaemon(True)
                self.stream_video.start()
            else:
                self.isStreaming = False
                self.url_stream = ""
                self.textEdit_url_1.setReadOnly(False)
                self.text_btn_url_1.setEnabled(True)
                self.stream_video.stop()
                self.label_stream.clear()
                self.status_lb_1.setText("Stream : Disabled")
                self.status_btn_1.setText("  Start Streaming  ")
                self.statusBar().showMessage("RTMP server disconnected", 2000)
        else:
            self.statusBar().showMessage("RTMP Server URL is Null!", 5000)

    def display_terrain(self):
        if(self.url_terrain != ""):
            if(self.isAnalysing is False):
                self.isAnalysing = True
                self.textEdit_url_2.setReadOnly(True)
                self.text_btn_url_2.setEnabled(False)
                self.status_lb_2.setText("Terrain : Enabled ")
                self.status_btn_2.setText("  Stop  Analysing  ")
                self.statusBar().showMessage("Analysing enabled", 5000)
                # threads can only be started once
                self.terrain_video = stream.StreamVideo(
                    self.url_terrain, self.label_terrain, self.terrain_width, self.terrain_height)
                self.terrain_video.setDaemon(True)
                self.terrain_video.start()
            else:
                self.isAnalysing = False
                self.url_terrain = ""
                self.textEdit_url_2.setReadOnly(False)
                self.text_btn_url_2.setEnabled(True)
                self.terrain_video.stop()
                self.label_terrain.clear()
                self.status_lb_2.setText("Terrain : Disabled")
                self.status_btn_2.setText("  Start Analysing  ")
                self.statusBar().showMessage("Analysing disabled", 2000)
        else:
            self.statusBar().showMessage("Terrain data source is Null!", 5000)

    def keyPressEvent(self, event):
        # print(event.text())
        if(event.key() == QtCore.Qt.Key_Up):
            self.statusBar().showMessage("Up", 500)
            self.send_command("0")
        elif(event.key() == QtCore.Qt.Key_Down):
            self.statusBar().showMessage("Down", 500)
            self.send_command("1")
        elif(event.key() == QtCore.Qt.Key_Left):
            self.statusBar().showMessage("Left", 500)
            self.send_command("2")
        elif(event.key() == QtCore.Qt.Key_Right):
            self.statusBar().showMessage("Right", 500)
            self.send_command("3")
        elif(event.key() == QtCore.Qt.Key_F11):
            self.full_screen()

    def send_command(self, signal):
        payload = {"direction": str(signal)}
        # Request_URL = "http://127.0.0.1:5000/"
        Request_URL = self.url_control
        if(not Request_URL or Request_URL != ""):
            try:
                response = requests.post(Request_URL, data=payload)
                if(response.status_code == requests.codes.ok):
                    print(response, str(response.text))
            except Exception:
                self.statusBar().showMessage("URL NOT FOUND", 5000)

    def URL_read(self):
        URL_1 = self.textEdit_url_1.toPlainText()
        URL_2 = self.textEdit_url_2.toPlainText()
        self.url_stream = URL_1
        self.url_terrain = URL_2

    def backend_connection(self):
        if(self.isControlling is False):
            self.isControlling = True
            self.textEdit_url_3.setReadOnly(True)
            self.text_btn_url_3.setText("Clear")
            URL = self.textEdit_url_3.toPlainText()
            self.url_control = URL
        else:
            self.isControlling = False
            self.textEdit_url_3.setReadOnly(False)
            self.text_btn_url_3.setText("Connect")
            self.url_control = ""

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
    # url = "rtmp://202.69.69.180:443/webcast/bshdlive-pc"

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
