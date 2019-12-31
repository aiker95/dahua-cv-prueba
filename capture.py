import numpy as np
import cv2 as cv
import time

url = "rtsp://admin:dahua2019@148.209.67.102:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
cap = cv.VideoCapture(url)
# cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("cannot open camera")
    exit()

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
name = '/Users/caves/PycharmProjects/dahua/videos/' + time.strftime('%d-%m-%Y_%X') + '.avi'
fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter(name, fourcc, 30, (width, height))

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame. Exiting...")
        break

    # Our operations on the frame come here
    out.write(frame)

    # Display the resulting frame
    cv.imshow("frame", frame)
    if cv.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv.destroyAllWindows()