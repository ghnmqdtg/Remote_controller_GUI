import cv2
import time
import threading
from PyQt5.QtGui import (QImage, QPixmap)


# this solution is inspired from stackoverflow:
# https://reurl.cc/MvrER4
class StoppableThread(threading.Thread):
    # inherit from threading.Thread
    # Thread class with a stop() method.
    # The thread itself has to check regularly for the stopped() condition.

    def __init__(self, url, out_label, width, height):
        super().__init__()
        self._stop_event = threading.Event()
        self.url = url
        self.out_label = out_label
        self.width = width
        self.height = height

    def stop(self):
        # set self._stop_event as True
        self._stop_event.set()

    def stopped(self):
        # if self._stop_event is True, return True
        return self._stop_event.is_set()


class StreamVideo(StoppableThread):

    def run(self):
        capture = cv2.VideoCapture(self.url)
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # FPS = 1/X
        # X = desired FPS
        FPS = 1 / 60
        FPS_MS = int(FPS * 1000)
        while(not self.stopped()):
            (status, frame) = capture.read()
            if(status):
                # resize the frame to fit the out.label
                frame = cv2.resize(frame, (self.width, self.height))
                # convert from RGB to BGR
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # The image is stored using a 24-bit RGB format (8-8-8).
                img = QImage(
                    frame.data,
                    frame.shape[1],
                    frame.shape[0],
                    QImage.Format_RGB888
                )
                # output image
                self.out_label.setPixmap(QPixmap.fromImage(img))
                # cv2.imshow("frame", frame)  # for debugging
                time.sleep(FPS)
                cv2.waitKey(FPS_MS)
            else:
                self.out_label.setText("URL not found")
                break


# for debugging
if __name__ == "__main__":
    url = "rtmp://202.69.69.180:443/webcast/bshdlive-pc"
    testthread = StreamVideo(url)
    testthread.start()
    time.sleep(10)
    testthread.stop()
