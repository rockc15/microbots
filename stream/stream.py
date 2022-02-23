import numpy as np
import cv2 as cv
import trackpy as tp
import pims
import matplotlib.pyplot as plt
from tp_plots import *  # module of modified trackpy plotting functions

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)    # convert frame to grayscale
    pim_gray = pims.frame.Frame(gray)   # turn grayscale into PIMS Frame object
    f = tp.locate(pim_gray, 13, invert=True)    # get feature location DataFrame
    fig = annotate(f, pim_gray).figure  # Get plt figure generated by trackpy's annotate

    # remove margins and axes from figure to only get annotated figure image
    ax = fig.gca()
    ax.axis('off')
    fig.tight_layout(pad=0)
    ax.margins(0)

    # Draw image onto plt canvas and convert into a numpy ndarray
    fig.canvas.draw()
    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    cv.imshow('frame', image_from_plot) # show annotated image
    fig.clear(True) # clear canvas for next preprocessed image

    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()