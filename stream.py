import cv2
import time
from PyQt5.QtGui import (QImage, QPixmap)

class StreamVideo(object):

    def __init__(self, url, out_label, width, height):
        self.capture = cv2.VideoCapture(url)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.out_label = out_label
        print(url)
        print(self.out_label)
        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 30
        self.FPS_MS = int(self.FPS * 1000)

    def output(self):
        while(self.capture.isOpened()):
            (status, frame) = self.capture.read()
            if(status):
                # convert from RGB to BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # The image is stored using a 24-bit RGB format (8-8-8).
                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.out_label.setPixmap(QPixmap.fromImage(img))
                time.sleep(self.FPS)
                cv2.waitKey(self.FPS_MS)
