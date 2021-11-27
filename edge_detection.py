# This is where the code that identifies candidate edges goes.
import sys
import cv2
import numpy as np


def show_img(im):
    cv2.imshow("", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_lines(im):
    # return cv2.filter2D(im, -1, np.asarray([[-.5, -7, -.5], [-1, -1, -1], [-.5, 7, -.5]]))
    # return cv2.filter2D(im, -1, np.asarray([[-2,-3,-2], [-1,-1,-1,], [1,3,1]]))
    return cv2.filter2D(im, -1, np.asarray([[1, 2, 1], [-.9, -.9, -.9], [-1, -2, -1]]))


def extract_lines(im):
    labels, connected = cv2.connectedComponents(im, connectivity=8)
    sizes = []
    points = []
    for x in range(1, labels):
        size = np.where(connected == x)[0].size
        sizes.append((x, size))
    sizes.sort(key=lambda d: d[1], reverse=True)
    for i, (x, s) in enumerate(sizes):
        if i <= (len(sizes) / 10):
            points.append([])
            for y_pos, x_pos in zip(np.where(connected == x)[0], np.where(connected == x)[1]):
                im[y_pos][x_pos] = 255
                points[i].append([y_pos, x_pos])
            # im[np.where(connected == x)] = 255
        else:
            im[np.where(connected == x)] = 0
    show_img(np.asarray(im, dtype=np.uint8))
    return points


if __name__ == '__main__':
    np.set_printoptions(threshold=sys.maxsize)
    if len(sys.argv) < 2:
        print(f'Pass in the path to the house image as the second argument!')
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        edges = get_lines(img)
        # show_img(edges)
        points = extract_lines(edges)
        print(points)

