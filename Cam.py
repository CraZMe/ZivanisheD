import os
import time

import cv2


class Camera:
    def __init__(self, sample_rate=0.01):
        self.sample_rate = sample_rate

    def record_camera(self):
        cap = cv2.VideoCapture()
        cap.open(0, cv2.CAP_DSHOW)
        count = 0
        while True:
            count += 1
            time.sleep(1)
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def configure_camera(self):
        os.system('python sample_video.py')
