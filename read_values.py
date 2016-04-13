from PIL import Image
import numpy, math
import scipy.misc as smp

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
	img = Image.open('data/voxels/vox390.MK.'+str(x)+'.'+str(y)+'.'+str(z)+'.tif')
	numpy_array = numpy.array(img)
	# image_array contains 260 arrays of values!
	image_array = normalise(numpy_array)

	return image_array


image_1 = process_image(7, 22, 0)
image_2 = process_image(7, 22, 1)
image_3 = process_image(7, 22, 2)
image_4 = process_image(7, 22, 3)
image_5 = process_image(7, 22, 4)
image_6 = process_image(7, 22, 5)

images = [process_image(7, 22, x) for x in range(0,71)]


def plot(images):
	new = Image.new('L', (260, 260))

	for i, image in enumerate(images):
		line = image[0]
		for x, value in enumerate(line):
			new.putpixel((x, i), (value * 2550))
	
	new.show()
	return

plot(images)



