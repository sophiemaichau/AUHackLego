"""
AUHack Lego 2018
By Jacob Schnedler, Mikkel Milo and Sophie Mai Chau
"""

import numpy as np
import cv2
import time

from detect_shapes import detect
from AUHack2018.SendOSCMessage import NoteSender


def object_intervals(cnts):
    if len(cnts) > 0:
        heights = [0] * len(cnts)
        x_intervals = [0] * len(cnts)
        for i in range(len(cnts)):
            y = [x[0][1] for x in cnts[i]]
            x = [x[0][0] for x in cnts[i]]
            x_intervals[i] = (min(x), max(x))
            diff_y = max(y) - min(y)
            heights[i] = diff_y
        return min(heights), max(heights), heights, x_intervals
    else:
        return None, None, None, None


def get_beats(x_intervals, image_width):
    beats = [x * int(image_width / 8) for x in range(0, 7)]
    #print('beats: ', beats)
    result = [0] * len(x_intervals)
    for i in range(len(x_intervals)):
        idx0 = np.array([x_intervals[i][0] < b for b in beats])
        idx1 = np.array([x_intervals[i][1] >= b for b in beats])
        intervals = np.logical_and(idx0, idx1)
        lower = np.argmax(intervals == 1)
        upper = lower + intervals.sum()
        result[i] = (lower, upper)
    return result


def tones(min_y, max_y):
    tone_list = [0] * 7
    size = max_y - min_y
    elem_size = size / 7
    for i in range(len(tone_list)):
        tone_list[i] = i * elem_size + min_y
    return tone_list


def map_cnts_to_tones(heights, tones):
    mapped_cnts = [0] * len(heights)
    for i in range(len(heights)):
        idxs = np.array([heights[i] >= t for t in tones])
        argmin = np.argmin([idxs == 1])
        if idxs.all() == 1:
            argmin = 7
        mapped_cnts[i] = argmin
    return mapped_cnts  # a list with numbers in [1,7]


def start_tracks(beats):
    if len(beats) > 4:
        beats = beats[0:3]
    ns0 = NoteSender(0, True)
    ns0.sendToSonicPi()
    for b in beats:
        ns = NoteSender(b[0], True)
        ns.notes = b[1:len(b)]
        ns.sendToSonicPi()
        time.sleep(0.2)


def set_disjunction(lst1, lst2):
    lst3 = [value for value in lst1 if value not in lst2]
    return lst3


def tone_nr_to_str(nr):
    if nr == 1: return 'A'
    if nr == 2: return 'B'
    if nr == 3: return 'C'
    if nr == 4: return 'D'
    if nr == 5: return 'E'
    if nr == 6: return 'F'
    if nr == 7: return 'G'


def beats_to_tracks(object_beats, tone_list):
    object_beats = list(zip(object_beats, tone_list))
    # print("zipped:", object_beats)
    track_intervals = []
    while len(object_beats) != 0:
        r = []
        # find smallest lower bound element
        lower_bounds = np.array([lower for ((lower, _), _) in object_beats])
        idx = np.argmin(lower_bounds)
        # print('idx', idx)
        r.append(object_beats[idx])

        object_beats.pop(idx)  # remove the beat with lowest lower bound
        # print('object_beats', object_beats)
        # now get all intervals that do not overlap with the one above. and add those to r
        remove_idxs = []
        for j in range(len(object_beats)):
            non_overlapping = [(y < object_beats[j][0][0] or x > object_beats[j][0][1]) for ((x, y), _) in r]
            if np.array(non_overlapping).all():
                r.append(object_beats[j])
                remove_idxs.append(j)
                # r = r + [(lower,upper) for (lower,upper) in object_beats if upper < r[0][0] or lower > r[0][1]]

        # object_beats = set_disjunction(object_beats, r) # remove all the elements from the above list
        for j in sorted(remove_idxs, reverse=True):
            del object_beats[j]

        track_intervals.append(r.copy())
        # print('r', r)

    # now construct the tracks
    res = []
    # print('track_intervals', track_intervals)
    for i in range(len(track_intervals)):
        track = track_intervals[i]
        tones = ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
        for j in track:
            a = j[0][0]
            b = j[0][1]
            # print(tones[a:b])
            c = j[1]
            for x in range(a, b):
                tones[x] = tone_nr_to_str(c)
        res.append([i + 1] + tones)
    return res


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
        if len(cnts) != 0:
            min_y, max_y, heights, x_intervals = object_intervals(cnts)
            tone_list = tones(min_y, max_y)
            mapped_cnts = map_cnts_to_tones(heights, tone_list)
            # print('tones: ', mapped_cnts)
            object_beats = get_beats(x_intervals, 300)
            # print('beats: ', object_beats)
            beats = beats_to_tracks(object_beats, mapped_cnts)
            start_tracks(beats)
        else:
            ns0 = NoteSender(0, True)
            ns0.sendToSonicPi()
        # Display the resulting frame
        # cv2.circle(cimg, (200, min_y), 3, (255, 0, 255), -1) # debugging heights
        # cv2.circle(cimg, (200, max_y), 3, (255, 0, 255), -1)
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
    tone_list = tones(min_y, max_y)
    mapped_cnts = map_cnts_to_tones(heights, tone_list)
    object_beats = get_beats(x_intervals, 300)
    print('object_beats:', object_beats)
    print('tracks:', beats_to_tracks(object_beats, mapped_cnts))


start_video_stream()
# draw_edges('lego.jpg')
