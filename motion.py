import cv2 as cv

ESC_KEY = 27

BORDER_COLOR = (0, 255, 0)  # green
BORDER_THICKNESS = 2

RESIZE_SCALE = 0.50

CONTOUR_AREA_THRESHOLD = 1000

FONT_SCALE = 1.5
FONT_COLOR = (0, 0, 255)  # red
FONT_THICKNESS = 3
FONT_LOCATION = (20, 40)


def main():
    cap = cv.VideoCapture('/Users/caves/Desktop/dahua/sample_videos/output-file.mp4')

    # read first two frames
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    if not ret:
        print('There was a problem reading the video file.')
        exit()

    while cap.isOpened():

        contours = get_contours(frame1, frame2)

        for contour in contours:
            (x, y, w, h) = cv.boundingRect(contour)

            if cv.contourArea(contour) < CONTOUR_AREA_THRESHOLD:
                continue

            cv.rectangle(frame1, (x, y), (x + w, y + h), BORDER_COLOR, BORDER_THICKNESS)
            cv.putText(frame1, "MOVIMIENTO", FONT_LOCATION, cv.FONT_HERSHEY_SIMPLEX, FONT_SCALE, FONT_COLOR, FONT_THICKNESS)

        # cv.drawContours(frame1, contours, -1, BORDER_COLOR, BORDER_THICKNESS)
        resized_frame = get_resized_frame(frame1)

        cv.imshow('feed', resized_frame)

        frame1 = frame2
        ret, frame2 = cap.read()

        if not ret:
            print('There was a problem reading the video file.')
            break

        if cv.waitKey(40) == ESC_KEY:
            break

    cv.destroyAllWindows()
    cap.release()


# functions
def get_contours(frame1, frame2):
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    return contours


def get_resized_frame(frame):
    width = int(frame.shape[1] * RESIZE_SCALE)
    height = int(frame.shape[0] * RESIZE_SCALE)
    dimensions = (width, height)
    resized = cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    return resized


if __name__ == '__main__':
    main()
