# This is where the code that identifies candidate edges goes.
import sys

import cv2
import numpy as np


def show_img(im):
    cv2.imshow("", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_lines(im):
    return cv2.filter2D(im, -1, np.asarray([[-1, -2, -1], [-1, 0, -1], [1, 2, 1]]))


def extract_lines(im):
    labels, connected = cv2.connectedComponents(im, connectivity=8)
    for x in range(1, labels):
        if np.where(connected == x)[0].size < 2:
            im[np.where(connected == x)] = 0
        else:
            im[np.where(connected == x)] = 255
    # im = cv2.dilate(im, np.ones((2,2)))
    show_img(np.asarray(im, dtype=np.uint8))


if __name__ == '__main__':
    np.set_printoptions(threshold=sys.maxsize)
    if len(sys.argv) < 2:
        print(f'Pass in the path to the house image as the second argument!')
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        # show_img(img)
        edges = get_lines(img)
        # show_img(edges)
        extract_lines(edges)



