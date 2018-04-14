"""
AUHack Lego 2018
By Jacob Schnedler, Mikkel Milo and Sophie Mai Chau
"""

import numpy as np
import cv2
from detect_shapes import detect


def object_intervals(cnts):
    heights = [0]*len(cnts)
    x_intervals = [0]*len(cnts)
    for i in range(len(cnts)):
        y = [x[0][1] for x in cnts[i]]
        x = [x[0][0] for x in cnts[i]]
        x_intervals[i] = (min(x),max(x))
        diff_y = max(y) - min(y)
        heights[i] = diff_y
    return min(heights), max(heights), heights, x_intervals

def get_beats(x_intervals, image_width):
    beats = [x*image_width/8 for x in range(0,7)]
    result = [0]*len(x_intervals)
    for i in range(x_intervals):
        idx0 = np.array([x_intervals[i][0] >= b for b in beats])
        idx1 = np.array([x_intervals[i][1] < b for b in beats])
        intervals = idx0 and idx1
        lower = np.argmax(intervals==1)
        upper = lower + intervals.sum()
        result[i] = (lower,upper)
    return result

def tones(min_y, max_y):
    tone_list = [0]*7
    size = max_y - min_y
    elem_size = size / 7
    for i in range(len(tone_list)):
        tone_list[i] = i * elem_size + min_y
    return tone_list

def map_cnts_to_tones(heights, tones):
    mapped_cnts = [0]*len(heights)
    for i in range(len(heights)):
        idxs = np.array([heights[i] >= t for t in tones])
        argmin = np.argmin([idxs==1])
        if idxs.all() == 1:
            argmin = 7
        mapped_cnts[i] = argmin
    return mapped_cnts # a list with numbers in [1,7]

def start_video_stream():
    cap = cv2.VideoCapture(1)
    w = int(cap.get(3))
    h = int(cap.get(4))

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Our operations on the frame come here
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cimg, cnts = detect(frame, hsv)
        min_y, max_y, heights, x_intervals = object_intervals(cnts)
        tone_list = tones(min_y, max_y)
        mapped_cnts = map_cnts_to_tones(heights, tone_list)
        #print('mapped_cnts', mapped_cnts)


        # Display the resulting frame
        #cv2.circle(cimg, (200, min_y), 3, (255, 0, 255), -1) # debugging heights
        #cv2.circle(cimg, (200, max_y), 3, (255, 0, 255), -1)
        cv2.imshow('AUHack LegoMusic', cimg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #cv2.waitKey()

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

# for testing
def draw_edges(im_path):
    image = cv2.imread(im_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cimg, cnts = detect(image, hsv)
    min_y, max_y, heights, x_intervals = object_intervals(cnts)
    object_beats = get_beats(x_intervals, 640) # 640 is hardcoded.
    tone_list = tones(min_y, max_y)
    print(object_beats)
    mapped_cnts = map_cnts_to_tones(heights, tone_list)

#start_video_stream()
draw_edges('lego.jpg')