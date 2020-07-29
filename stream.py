import cv2
import time


class StreamVideo(object):

    def __init__(self, src):
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        # FPS = 1/X
        # X = desired FPS
        self.FPS = 1 / 30
        self.FPS_MS = int(self.FPS * 1000)

    def show_frame(self):
        (self.status, self.frame) = self.capture.read()
        cv2.imshow("frame", self.frame)
        time.sleep(self.FPS)
        cv2.waitKey(self.FPS_MS)


if __name__ == "__main__":
    src = "rtmp://202.69.69.180:443/webcast/bshdlive-pc"
    stream_video = StreamVideo(src)
    while True:
        try:
            stream_video.show_frame()
        except AttributeError:
            pass
