# William Keilsohn
# September 4 2025

# Import Packages
import os

# Declare Variables
cpath = os.getcwd()
impath = os.path.join(cpath, "Images")

base_name = "butterfly"
extension = ".jpg"

files = [f for f in os.listdir(impath) if f.lower().endswith(extension)]

# Declare Functions
def renamer(files):
	global impath
	global base_name
	global extension
	total = len(files)
	digits = len(str(total))
	for i, filename in enumerate(files, start=1):
		old_path = os.path.join(impath, filename)
		new_filename = f"{base_name}{i:0{digits}d}{extension}"  # Zero-padded
		new_path = os.path.join(impath, new_filename)
		os.rename(old_path, new_path)
		comp_per = str((i / total) * 100) + "%" # Percentage Complete
		print(comp_per)
        
# Run Application
if __name__=='__main__':
	files.sort()
	renamer(files=files)