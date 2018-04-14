"""
AUHack Lego 2018
By Jacob Schnedler, Mikkel Milo and Sophie Mai Chau
"""

import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt
from skimage import feature
from skimage import measure
from skimage import io
from skimage.io import imsave
from detect_shapes import detect

def start_video_stream():
    cap = cv2.VideoCapture(1)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        cimg = cv2.flip(frame, 1) # flipping it vertically
        hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)
        imsave('hsv.jpg', hsv)
        cimg = detect(cimg, hsv)

        # Display the resulting frame
        cv2.imshow('AUHack LegoMusic', cimg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# for testing
def draw_edges(im_path):
    image = cv2.imread(im_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detect(image, hsv)

start_video_stream()
#draw_edges('lego.jpg')