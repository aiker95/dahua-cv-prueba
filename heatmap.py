import cv2 as cv
import numpy as np
import copy

from motion import get_resized_frame


def main():
    cap = cv.VideoCapture('/Users/caves/Desktop/dahua/sample_videos/output-file.mp4')
    fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

    # number of frames is a variable for development purposes, you can change the for loop to a while(cap.isOpened())
    # instead to go through the whole video
    FRAMES = 5000

    first_iteration_indicator = 1
    for i in range(0, FRAMES):
    # while cap.isOpened():
        '''
        There are some important reasons this if statement exists:
            -in the first run there is no previous frame, so this accounts for that
            -the first frame is saved to be used for the overlay after the accumulation has occurred
            -the height and width of the video are used to create an empty image for accumulation (accum_image)
        '''

        ret, frame = cap.read()
        frame = get_resized_frame(frame)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        if first_iteration_indicator == 1:
            first_frame = copy.deepcopy(frame)
            height, width = gray.shape[:2]
            accum_image = np.zeros((height, width), np.uint8)
            first_iteration_indicator = 0
        else:
            fgmask = fgbg.apply(gray)  # remove the background

            # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you
            # want motion to be picked up more, increase the value of maxValue.  To pick up the least amount of
            # motion over time, set maxValue = 1
            thresh = 2
            max_value = 1
            ret, th1 = cv.threshold(fgmask, thresh, max_value, cv.THRESH_BINARY)

            # add to the accumulated image
            accum_image = cv.add(accum_image, th1)

            # testing
            # for testing purposes, show the result of the background subtraction
            # cv.imshow('diff-bkgnd-frame', fgmask)

            # for testing purposes, show the threshold image
            # cv.imwrite('diff-th1.jpg', th1)

            # for testing purposes, show the accumulated image
            # cv.imwrite('diff-accum.jpg', accum_image)

            # for testing purposes, control frame by frame
            # input("press any key to continue")

        # for testing purposes, show the current frame
        # cv.imshow('frame', gray)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # apply a color map
    # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
    color_image = cv.applyColorMap(accum_image, cv.COLORMAP_HOT)

    # for testing purposes, show the colorMap image
    # cv2.imwrite('diff-color.jpg', color_image)

    # overlay the color mapped image to the first frame
    result_overlay = cv.addWeighted(first_frame, 0.7, color_image, 0.7, 0)

    # save the final overlay image
    cv.imwrite('diff-overlay.jpg', result_overlay)

    # cleanup
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
