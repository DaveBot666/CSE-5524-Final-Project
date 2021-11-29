from place_lights import place_multiple_light_strands, get_super_pixels_and_superpixel_colors
from edge_detection import extract_lines, get_lines
from PIL import Image
import cv2
import numpy as np
import sys

def my_key(point):
	return point[0]

def has_positive(arr):
	for a in arr:
		if a > 0:
			return True

	return False

def has_negative(arr):
	for a in arr:
		if a < 0:
			return True

	return False

def relevant_feature(points, i, j, back=5):
	vals = [points[i][j-m][1]-points[i][j-m-1][1] for m in range(back)]
	b1 = (vals[-1] != 0)
	b2 = has_positive(vals)
	b3 = has_negative(vals)
	b4 = abs(sum(vals[:-1]))>int(back/5)
	ret = b1 and ((b2 and not b3) or (b3 and not b2)) and b4
	return ret

def dist(p1, p2):
	return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def extract_points(file_path):
	house_cv = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
	house_width = house_cv.shape[1]
	house_height = house_cv.shape[0]
	edges = get_lines(house_cv)
	points = extract_lines(edges)
	points_2 = [[[points[i][j][1], points[i][j][0]] for j in range(len(points[i]))] for i in range(len(points))]
	for i in range(len(points_2)):
		points_2[i].sort(key=my_key)

	back = 8
	points_3 = []
	for i in range(len(points_2)):
		x_max = 0
		x_min = 0
		y_max = 0
		extra_points = []
		prev_extra = False
		for j in range(1, len(points_2[i])):
			if points_2[i][j][0] > points_2[i][x_max][0]:
				x_max = j

			if points_2[i][j][1] < points_2[i][y_max][1]:
				y_max = j

			if points_2[i][j][0] < points_2[i][x_min][0]:
				x_min = j

			if j>back and relevant_feature(points_2, i, j, back=back):
				if not prev_extra:
					extra_points.append(j)

				prev_extra = True
			else:
				prev_extra = False

		e1 = []
		e2 = []
		for c in range(len(extra_points)):
			if extra_points[c]>x_min and extra_points[c]<y_max:
				if len(e1)==0 or points_2[i][extra_points[c]][0]-e1[-1][0]>10:
					e1.append(points_2[i][extra_points[c]])
			elif extra_points[c]>y_max and extra_points[c]<x_max:
				if len(e2)==0 or points_2[i][extra_points[c]][0]-e2[-1][0]>10:
					e2.append(points_2[i][extra_points[c]])


		p = []

		if (y_max==x_min or y_max==x_max) and x_min!=x_max:
			p = [points_2[i][x_min], *e1, points_2[i][x_max]]

		elif x_min!=x_max:
			p = [points_2[i][x_min], *e1, points_2[i][y_max], *e2, points_2[i][x_max]]

		if len(p)>0 and points_2[i][y_max][1]<4/5*house_height:
			dp = sum([dist(p[i], p[i-1]) for i in range(len(p)-1)])
			if dp > house_width/30:
				points_3.append(p)
		

	return points_3

np.set_printoptions(threshold=sys.maxsize)
if len(sys.argv) < 2:
    print(f'Pass in the path to the house image as the second argument!')
    exit()

house_path = sys.argv[1]

house = Image.open(house_path)



light = Image.open(r"Lights/white_light.png")

points = extract_points(house_path)
x = len(points)

segments_slic, super_pixels_color = get_super_pixels_and_superpixel_colors(house)

for i in range(x):
	house = place_multiple_light_strands(house, light, points[i], segments_slic, super_pixels_color)
	print((i+1)/x*100, "%")


house.show()