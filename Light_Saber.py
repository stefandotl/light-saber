import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
# cap = cv2.VideoCapture('chaplin.mp4')
cap = cv2.VideoCapture(0)

def emptyFunction():
	"""needed for trackbar"""
	pass

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

windowName = 'Frame'
cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
cv2.createTrackbar('Low_Blue', windowName, 32, 255, emptyFunction)
cv2.createTrackbar('High_Blue', windowName, 66, 255, emptyFunction)
cv2.createTrackbar('Low_Green', windowName, 113, 255, emptyFunction)
cv2.createTrackbar('High_Green', windowName, 255, 255, emptyFunction)
cv2.createTrackbar('Low_Red', windowName, 92, 255, emptyFunction)
cv2.createTrackbar('High_Red', windowName, 254, 255, emptyFunction)


# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # values of blue, green, red
        low_blue = cv2.getTrackbarPos('Low_Blue', windowName)
        high_blue = cv2.getTrackbarPos('High_Blue', windowName)
        low_green = cv2.getTrackbarPos('Low_Green', windowName)
        high_green = cv2.getTrackbarPos('High_Green', windowName)
        low_red = cv2.getTrackbarPos('Low_Red', windowName)
        high_red = cv2.getTrackbarPos('High_Red', windowName)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        low_color = np.array([low_blue, low_red, low_green])
        up_color = np.array([high_blue, high_red, high_green])
        mask = cv2.inRange(hsv, low_color, up_color)


        # ret, thresh_image = cv2.threshold(hsv, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 200:
                # rect = cv2.minAreaRect(cnt)
                # box = cv2.boxPoints(rect)
                # box = np.int0(box)
                hull = cv2.convexHull(cnt)
                # cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                cv2.drawContours(frame, [hull], -1, (0,255,0), -1)

        # my implementation, does it wait 1000 milli-seconds?
        # cv2.imwrite("neues Bild", frame)
        # cv2.waitKey(1000)

        cv2.imshow('Thresh', mask)
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # Press "X" on window to exit
        if cv2.getWindowProperty('Frame',cv2.WND_PROP_VISIBLE) < 1:
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()
# Closes all the frames
cv2.destroyAllWindows()
