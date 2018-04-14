"""
AUHack Lego 2018
By Jacob Schnedler, Mikkel Milo and Sophie Mai Chau
"""

import numpy as np
import cv2
import imutils

def start_video_stream():
    cap = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #gray = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2GRAY)  # making the image grey and flipping it vertically
        #gray = imutils.resize(gray, width=400)
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(gray, 'Lego', (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('AUHack LegoMusic', cv2.flip(frame, 1))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

start_video_stream()