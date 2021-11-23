# This is where the code that identifies candidate edges goes.
import sys

import cv2
import numpy as np
from scipy import ndimage


def show_img(im):
    cv2.imshow("image", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_lines(im):
    return cv2.filter2D(im, -1, np.asarray([[-1, -2, -1], [-1, 0, -1], [1, 2, 1]])).astype(float) / 255


def extract_lines(im):
    erode = cv2.erode(im, np.ones((1, 1), np.uint8), iterations=1)
    dilate = cv2.dilate(erode,  np.ones((3, 3), np.uint8), iterations=1)
    connected = cv2.connectedComponents(dilate)

        



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Pass in the path to the house image as the second argument!')
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        show_img(img)
        edges = get_lines(img)
        show_img(edges)
        extract_lines(edges)



