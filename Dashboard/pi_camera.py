import cv2
import time
import numpy as np

class VideoCamera(object):

    global video 
    video = cv2.VideoCapture(0)

    def __del__():
        video.release()

    def get_frame():
        return video.read()
    
    def get_photo():
        success, image = video.read()
        if not success:
            pass
        else:
            return image