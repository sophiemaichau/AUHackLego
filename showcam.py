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
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cimg, cnts = detect(frame, hsv)
        min_y, max_y = radius(cnts)

        # Display the resulting frame
        cv2.circle(cimg, (200, min_y), 3, (255, 0, 255), -1)
        cv2.circle(cimg, (200, max_y), 3, (255, 0, 255), -1)
        cv2.imshow('AUHack LegoMusic', cimg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def radius(cnts):
    r = [0]*len(cnts)
    for i in range(len(cnts)):
        y = [x[0][1] for x in cnts[i]]
        diff = max(y) - min(y)
        r[i] = diff
    return min(r), max(r)

# for testing
def draw_edges(im_path):
    image = cv2.imread(im_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cimg, cnts = detect(image, hsv)
    min_y, max_y = radius(cnts)
    print('min, max: ', min_y, max_y)

start_video_stream()
#draw_edges('lego.jpg')