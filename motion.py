import cv2 as cv

ESC_KEY = 27
GREEN = (0, 255, 0)
BORDER_THICKNESS = 2

cap = cv.VideoCapture('/Users/caves/Desktop/dahua/sample_videos/output-file.mp4')

# read first two frames
ret, frame1 = cap.read()
ret, frame2 = cap.read()

if not ret:
    print('There was a problem reading the video file.')
    exit()

while cap.isOpened():
    # get contours for the moving elements
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(frame1, contours, -1, GREEN, BORDER_THICKNESS)

    # resize
    scale_percent = 50  # percent of original size
    width = int(frame1.shape[1] * scale_percent / 100)
    height = int(frame1.shape[0] * scale_percent / 100)
    dimensions = (width, height)

    resized = cv.resize(frame1, dimensions, interpolation=cv.INTER_AREA)

    cv.imshow('feed', resized)
    frame1 = frame2
    ret, frame2 = cap.read()

    if not ret:
        print('There was a problem reading the video file.')
        break

    if cv.waitKey(40) == ESC_KEY:
        break

cv.destroyAllWindows()
cap.release()