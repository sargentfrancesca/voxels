from PIL import Image
import numpy, math, sys

sys.path.append("/opt/minecraft-pi/api/python/")
     
from dbscode_minecraft import *
from mcpi import minecraft
from mcpi.block import *

mc = minecraft.Minecraft.create()

def bulldoze():
	size=255
	height=255 
	print("bulldozing")
	mc.setBlocks(-size/2,0,-size/2,size/2,height,size/2,AIR)
	# mc.setBlock(-size/2, -1, -size/2, size, 1, size, GRASS)
	# change this
	box(GRASS,point(-size/2,-1,-size/2),point(size,1,size))
	print("finished bulldozing")
	
bulldoze()

# Size, always square
size = 260
# X value of source tile
x_val = 21
# Y value of source tile
y_val = 21  
# Max Z value of source tile
z_val = 70
# X value to start crop
crop_x = 0
# Y value to start crop
crop_y = 0

def convert(old_value):
	old_max = 1
	old_min = 0
	new_max = 15
	new_min = 0
	old_range = old_max - old_min
	new_range = new_max - new_min
	value = (((old_value - old_min) * new_range) / old_range) + new_min
	return int(value)
	
# Find minimum and maximum of image
def find_min_max(array):
	mins_maxs = []
	for line in array:
		mins_maxs.append(min(line))
		mins_maxs.append(max(line))
	return min(mins_maxs), max(mins_maxs)

# Removing 'nan' from lists - replacing with 0.0 for now, creating new array
def normalise(array):
	data = []
	for line in array:
		new_items = [x if not math.isnan(x) else 0 for x in line]
		data.append(new_items)
	return data
	
# converting TIFF into arrays that we can work with
def process_image(x, y, z):  
	# Open image, convert to numpy array
	img = Image.open('tif/LT_21.21/vox390.LT.'+str(x)+'.'+str(y)+'.'+str(z)+'.tif')
	numpy_array = numpy.array(img)
	# image_array contains 260 arrays of values!
	image_array = normalise(numpy_array)

	return image_array

# create an array of each image for this section
images = [process_image(x_val, y_val, x) for x in range(0,z_val + 1)]
def material(value, x, y, i):
	if value > 0.2:
		mc.setBlocks(x-127,i,y-127,((x+1) - 127),i+1,((y+1) - 127), WOOL.id, 3)
	
def png_convert(images):
	for i, image in enumerate(images):
		print "layer", i
		for x, line in enumerate(image):
			for y, value in enumerate(line):
				# new.putpixel((x, y), ((convert(value)), (convert(value)), (convert(value)), (convert(value))))
				# box(material(value), point(float(x), float(i), float(y)), point(1,1,1))
				material(value, x, y, i)
		print "layer", i, "complete"
	
	return

png_convert(images)
