#This will be were the code for placing lights on the image will go
from PIL import Image
import numpy as np
import copy
from math import ceil
import random
from skimage.segmentation import slic
from skimage import io

def get_super_pixels_and_superpixel_colors(house: Image):
	n_segments=int(np.sqrt(house.size[0]*house.size[1]))
	house_np = np.array(house)
	segments_slic = slic(house_np, n_segments=n_segments, compactness=10, start_label=0)
	
	counts = np.array([0 for i in range(n_segments)])
	colors = np.array([[0, 0, 0] for i in range(n_segments)])
	for n in range(len(house_np)):
		for m in range(len(house_np[n])):
			classifier = segments_slic[(n, m)]
			counts[classifier]+=1 
			colors[classifier]+=house_np[n][m]

	return segments_slic, np.array([colors[i]/counts[i] if counts[i]>0 else colors[i] for i in range(len(colors))])



def place_light_strand_on_house(house: Image, light_strand: Image, start: list, end: list, segments_slic: np.array, super_pixels_color: list) -> Image:
	"""Returns an image of @house with image @light_strand overlayed
	from point start to point end.

	Requires:
		end[0] < house.size[0] and end[1] < house.size[1] and
		start[0] < house.size[0] and start[1] < house.size[1]

    Args:
		house: PIL image of house
		light_strand: PIL image of light strand with alpha layer for background
		start: Starting point for the light strand
		end: End point for the light strand

    Returns:
    	PIL Image with an image of the house with the light stand from point
    	start to point end on the house image.

    """
	if start[0]>end[0]:
		temp = start
		start=end
		end=temp

	w = int(np.sqrt(sum([(e-s)**2 for e, s in zip(end, start)])))
	h = int(w/light_strand.size[0]*light_strand.size[1])
	
	theta = -np.arctan2(end[1]-start[1], end[0]-start[0])/np.pi*180

	light_strand =light_strand.resize((w, h), Image.ANTIALIAS)
	offset_x = int(-np.sin(theta/180*np.pi)*light_strand.size[1])
	offset_y = 0


	light_strand = light_strand.rotate(theta, Image.NEAREST, expand = 1)

	if theta>0:
		offset_y = light_strand.size[1]-h



	ret = copy.deepcopy(house)

	ret.paste(light_strand, (start[0]-offset_x, start[1]-offset_y), mask = light_strand)

	return ret


def place_multiple_light_strands(house: Image, light: Image, points: list, segments_slic: np.array, super_pixels_color: list):
	"""Returns an image of @house with image @light_strand overlayed
	from point to point in @points

	Requires:
		point[0] < house.size[0] and point[1] < house.size[1] for point in points

	Args:
		house: PIL image of house
		light_strand: PIL image of light strand with alpha layer for background
		points: list of points

	Returns:
		PIL Image with an image of the house with the light stand from point
		start to point end on the house image.

	"""
	ret = copy.deepcopy(house)
	for i in range(len(points)-1):
		light_strand = create_strand(house, light, points[i], points[i+1], segments_slic, super_pixels_color)
		ret = place_light_strand_on_house(ret, light_strand, points[i], points[i+1], segments_slic, super_pixels_color)

	return ret


def color_light(house: Image, point: list or tuple, segments_slic: np.array, super_pixels_color: list):
	"""Returns the 1 - average color of the @house in the region of the super pixel
	in @segment_slices of the @point in @house.

	Requires:
		point[0] < house.size[0] and point[1] < house.size[1] -
		and
		@segments_slice is a superpixels representation of @house

	Args:
		house: PIL image of house
		point: point of interest whose regions average color we would like to return.


	Returns:
		An RGBA value that has the 1 - average color of the superpixel region of @point
		on a scale from 0 to 1 with and alpha value of 1.

	"""
	img = np.array(house)
	if point[0] >= len(img):
		point = (len(img)-1, point[1])

	if point[1] >= len(img[0]):
		point = (point[0], len(img[0])-1)

	color = super_pixels_color[segments_slic[point]]
	a = min(color)
	b = max(color)
	color = [1-(c-a)/(b-a) for c in color]
	return [*color, 1]


def create_strand(house: Image, light: Image, start: list, end: list, segments_slic: np.array, super_pixels_color: list):
	"""
	Requires:
		start[0] < house.size[0] and start[1] < house.size[1] 
		and
		end[0] < house.size[0] and end[1] < house.size[1] 

	Args:
		house: PIL image of house
		start: Starting point for the light strand
		end: End point for the light strand

	Returns:
		A light strand with lights colored to 

	"""
	w = int(np.sqrt(sum([(e-s)**2 for e, s in zip(end, start)])))
	dist = 5
	lights = ceil(w/dist)
	ret = Image.new(mode='RGBA', size=(light.size[0]*lights, light.size[1]), color=(0, 0, 0, 0))
	mask = np.array(copy.deepcopy(light))
	img = np.array(house)
	
	theta = np.arctan2(end[1]-start[1], end[0]-start[0])

	for c in range(lights):
		x = int(c*dist*np.cos(theta)+start[0])
		y = int(c*dist*np.sin(theta)+start[1])
		point = (y, x)
		light_temp = np.array(copy.deepcopy(light))
		p = [0, 0, 0, 0]
		color_mask = color_light(house, point, segments_slic, super_pixels_color)
		for i in range(1, len(mask)-1):
			for j in range(1, len(mask[i])-1):
				pix = light_temp[i, j]*color_mask			

				light_temp[i][j] = pix

		ret.paste(Image.fromarray(light_temp), (c*light.size[0], 0), mask = Image.fromarray(light_temp))

	return ret