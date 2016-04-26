from PIL import Image
import numpy, math
import scipy.misc as smp
import sys, os

# Size, always square
size = int(sys.argv[1])
# X value of source tile
x_val = int(sys.argv[2])
# Y value of source tile
y_val = int(sys.argv[3])
# Max Z value of source tile
z_val = int(sys.argv[4])
# X value to start crop
crop_x = int(sys.argv[5])
# Y value to start crop
crop_y = int(sys.argv[6])

# range conversion - not so effective, but could be used elsewhere...
def convert(old_value):
	old_max = 1
	old_min = 0
	new_max = 255
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
	img = Image.open('data/voxels/all_mk/vox390.MK.'+str(x)+'.'+str(y)+'.'+str(z)+'.tif')
	numpy_array = numpy.array(img)
	# image_array contains 260 arrays of values!
	image_array = normalise(numpy_array)

	return image_array

# create an array of each image for this section
images = [process_image(x_val, y_val, x) for x in range(0,z_val + 1)]


def plot_cross(images, l):
	# creating new grayscale image
	new = Image.new('L', (260, 260))

	# enumerate over images
	for i, image in enumerate(images):
		# grab 'line' of image
		line = image[l]
		for x, value in enumerate(line):
			# place pixel in x position, at image index, with density value
			new.putpixel((x, 259 - i), (value * (255 * 5)))
	new.save("data/voxels/cross/mk-7-23/mk-7-23-{0:04d}.png".format(l))
	return

def png_convert(images):
	new = Image.new('RGBA', (260, 260))

	for i, image in enumerate(images):
		for x, line in enumerate(image):
			for y, value in enumerate(line):
				new.putpixel((x, y), ((convert(value)), (convert(value)), (convert(value)), (convert(value))))
				w, h = new.size
				new_image = new.crop((crop_x, crop_y, crop_x + size, crop_y + size))
				resized = new_image.resize((50, 50), Image.ANTIALIAS)

	
		directory = "data/voxels/png/mk-"+str(x_val)+"-"+str(y_val)+"/crop/"+str(size) + str(crop_x) + str(crop_y)
		if not os.path.exists(directory):
			os.makedirs(directory)

		filename = "mk"+str(i)+".png"
		print directory, filename
		resized.save(directory + "/" + filename)

# creates 260 images
# for i in range(0, 259):
# 	# i = 'line' of image
# 	png_convert(images, i)

png_convert(images)


