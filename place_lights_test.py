from place_lights import place_light_strand_on_house 
from PIL import Image

	
def test_1():
	"""
	Should show 2 identical images with lights going from the upper left toward 
	the middle at a 45 degree angle to the (50, 50) point on the house.
	"""
	house = Image.open(r"Train Images/test1.jpg")

	light_strand = Image.open(r"Lights/lights2.png")

	start = [0, 0]

	end = [50, 50]


	house = place_light_strand_on_house(house, light_strand, start, end)

	house.show()

	start = [50, 50]

	end = [0, 0]


	house = place_light_strand_on_house(house, light_strand, start, end)

	house.show()

def test_2():
	"""
	Should show the strand of lights going all the way from the upper left to upper right
	of the house image.
	"""
	house = Image.open(r"Train Images/test1.jpg")

	light_strand = Image.open(r"Lights/lights2.png")

	start = [0, house.size[1]]

	end = [house.size[0], 0]


	house = place_light_strand_on_house(house, light_strand, start, end)

	house.show()



test_2()