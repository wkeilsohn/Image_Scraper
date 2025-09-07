# William Keilsohn
# September 5 2025

# Import Packages
import os
from PIL import Image

# Define Variables
cpath = os.getcwd()
new_size = (560, 560)

# Run Application

if __name__=="__main__":
	for root, dirs, files in os.walk(os.path.join(cpath, "Images")):
		for file in files:
			if file.endswith('.jpg'):
				full_file_path = os.path.join(root, file)
				image = Image.open(full_file_path)
				resized_image = image.resize(new_size, Image.LANCZOS)
				resized_image.save(full_file_path, quality=95)