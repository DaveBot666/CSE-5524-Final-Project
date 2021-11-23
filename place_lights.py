#This will be were the code for placing lights on the image will go
from PIL import Image
import numpy as np
import copy

def place_light_strand_on_house(house: Image, light_strand: Image, start: list, end: list) -> Image:
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
	offset_x = 0
	offset_y = 0


	light_strand = light_strand.rotate(theta, Image.NEAREST, expand = 1)

	if theta>0:
		offset_y = light_strand.size[1]-h

	ret = copy.deepcopy(house)

	ret.paste(light_strand, (start[0]-offset_x, start[1]-offset_y), mask = light_strand)

	return ret

