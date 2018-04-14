# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2


def find_frequencies(shapes, ratio):
    max_x = 0
    max_y = 0
    min_x = 9001
    min_y = 9001
    xs = []
    ys = []
    for c in shapes:
        M = cv2.moments(c)
        M["m00"] = 1 if M["m00"] == 0 else M["m00"]
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        xs.append(cX)
        ys.append(cY)
        max_x = max(max_x, cX)
        max_y = max(max_y, cY)
        min_x = min(min_x, cX)
        min_y = min(min_y, cY)
        #print(cX, ",", cY)

    # ratios are close to 1 if close to max, and closer to 0 if close to min.
    x_ratios = [x / max_x for x in xs]
    y_ratios = [y / max_y for y in ys]
    return x_ratios


def run_opencv_detect_shapes(img_path):
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to the input image")
    args = vars(ap.parse_args())

    # load the image and resize it to a smaller factor so that
    # the shapes can be approximated better
    image = cv2.imread(args["image"])
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = 255 - cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", gray)
    cv2.waitKey()
    blurred = cv2.GaussianBlur(gray, (5, 5), 10)
    thresh = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Image", thresh)
    cv2.waitKey()


    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()


    print("frequencies:", find_frequencies(cnts, ratio))
    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        M["m00"] = 1 if M["m00"] == 0 else M["m00"]
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 2)

        # show the output image
        cv2.imshow("Image", image)
    cv2.waitKey()
run_opencv_detect_shapes(".")


def show_opencv_detect_shapes(image):
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    gray = 255 - cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 10)
    thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    sd = ShapeDetector()

    # loop over the contours
    for c in cnts:
        # compute the center of the contour, then detect the name of the
        # shape using only the contour
        M = cv2.moments(c)
        print(M["m00"])
        #cX = int((M["m10"] / M["m00"]) * ratio)
        #cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)

        # multiply the contour (x, y)-coordinates by the resize ratio,
        # then draw the contours and the name of the shape on the image
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        #cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
        #            0.5, (255, 255, 255), 2)

        # show the output image
        cv2.imshow("Image", image)


