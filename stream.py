import cv2
import time
from PyQt5.QtGui import (QImage, QPixmap)

class StreamVideo(object):

    def __init__(self, url, out_label, width, height, flag):
        self.capture = cv2.VideoCapture(url)
        self.width = width
        self.height = height
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.out_label = out_label
        self.isStreaming = flag
        # print(url)
        # print(self.out_label)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 60
        self.FPS_MS = int(self.FPS * 1000)

    def output(self, ):
        time.sleep(1)
        while(self.isStreaming):
            (status, frame) = self.capture.read()
            if(status):
                # convert from RGB to BGR
                frame = cv2.resize(frame, (self.width, self.height))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # The image is stored using a 24-bit RGB format (8-8-8).
                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.out_label.setPixmap(QPixmap.fromImage(img))
                time.sleep(self.FPS)
                cv2.waitKey(self.FPS_MS)
            else:
                break
