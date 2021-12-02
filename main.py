from place_lights import place_multiple_light_strands, get_super_pixels_and_superpixel_colors, color_light
from edge_detection import extract_lines, get_lines
from PIL import Image
import cv2
import numpy as np
import sys
from skimage import io


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
	b4 = abs(sum(vals[:-1]))>0
	ret = b1 and ((b2 and not b3) or (b3 and not b2)) and b4
	return ret

def dist(p1, p2):
	return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def extract_points(file_path, my_filter=np.array([[1, 2, 1], [-.9, -.9, -.9], [-1, -2, -1]])):
	house_cv = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
	house_width = house_cv.shape[1]
	house_height = house_cv.shape[0]
	edges = get_lines(house_cv, my_filter)
	Image.fromarray(edges).show()
	points = extract_lines(edges)
	points_2 = [[[points[i][j][1], points[i][j][0]] for j in range(len(points[i]))] for i in range(len(points))]
	for i in range(len(points_2)):
		points_2[i].sort(key=my_key)

	back = 5
	points_3 = []
	for i in range(len(points_2)):
		p = []

		for j in range(int(len(points_2[i])/10)):
			t=j*10
			p.append(points_2[i][t])

		if t<len(points_2):
			p.append(points_2[i][-1])

		if len(p)>0 and points_2[i][0][1]<3/4*house_height and points_2[i][-1][1]<3/4*house_height:
			dp = sum([dist(p[i], p[i-1]) for i in range(len(p)-1)])
			if dp > house_width/25:
				points_3.append(p)
		

	return points_3

np.set_printoptions(threshold=sys.maxsize)
if len(sys.argv) < 2:
    print(f'Pass in the path to the house image as the second argument!')
    exit()



house_path = sys.argv[1]

house = Image.open(house_path)

house_copy = Image.open(house_path)

w=house_copy.size[0]

h=house_copy.size[1]

scale=1

while w/scale>500 and h/scale>500:
	scale*=2

temp_name = "temp.jpg"

house_copy = house_copy.resize((int(w/scale), int(h/scale)), Image.ANTIALIAS)

house_copy.save(temp_name)

light = Image.open(r"Lights/white_light.png")

print("Extracting Points")

filters = []
cent = -.9
# filters.append(np.array([[-2, -1, -.9],[-1, -.9, 1],[-.9, 1, 2]]))
# filters.append(np.array([[-.9, -1, -2],[1, -.9, -1],[2, 1, -.9]]))
filters.append(np.array([[1, 2, 1], [cent, cent, cent], [-1, -2, -1]]))
filters.append(np.array([[-1, -2, -1], [cent, cent, cent], [1, 2, 1]]))

points = []
for f in filters:
	ps = extract_points(temp_name, f) 
	for p in ps:
		points.append(p)

x = len(points)

for i in range(len(points)):
	for j in range(len(points[i])):
		points[i][j][0]=int(points[i][j][0]*scale)
		points[i][j][1]=int(points[i][j][1]*scale)

print("Generating Color Scheme")
segments_slic, super_pixels_color = get_super_pixels_and_superpixel_colors(house)
sp = []
y = len(segments_slic)
for i in range(y):
	sp.append([])
	for j in range(len(segments_slic[i])):
		color = super_pixels_color[segments_slic[i][j]]
		a = min(color)
		b = max(color)
		color = [255-(c-a)*255/(b-a) for c in color]
		sp[i].append(color)
	print((i+1)/y*100, "%")

sp = np.array(sp)
print(sp.shape)
io.imsave("super_pixel_color_mask.png", sp)
io.show()
print("Placing Lights")
for i in range(x):
	house = place_multiple_light_strands(house, light, points[i], segments_slic, super_pixels_color)
	print((i+1)/x*100, "%")


house.show()