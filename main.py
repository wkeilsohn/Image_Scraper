# William Keilsohn
# September 3 2025

# Import Packages
import os
import requests as req
from bs4 import BeautifulSoup
import time

# Declare Variables
url = "https://bugguide.net/node/view/540/bgimage?from={}"
cpath = os.getcwd()
impath = os.path.join(cpath, "Images")

# Declare Functions
def call_web(image_num):
	global url
	new_url = url.format(image_num)
	try:
		resp = req.get(new_url)
		if resp.status_code == 200:
			return resp.text
		else:
			print(resp.status_code)
	except Exception as e:
		print(e)
		
def call_image_page(url):
	try:
		resp = req.get(url)
		if resp.status_code == 200:
			print(url)
			return resp.text
		else:
			print(resp.status_code)
	except Exception as e:
		print(e)

def find_image_section(raw_text):
	bottom = raw_text.split('title="Species"')[1]
	middle = bottom.split("</td></tr></table>")[0]
	return middle
	
def extract_image_links(raw_txt):
	soup = BeautifulSoup(raw_txt, 'html.parser')
	image_links = []
	for img in soup.find_all('a', href=True):
		image_links.append(img['href'])
	return image_links
	
def extract_central_image_link(raw_text):
	soup = BeautifulSoup(raw_text, 'html.parser')
	image_links = []
	img_tags =soup.find_all("img")
	for img in img_tags:
		src = img.get('src')
		image_links.append(src)
	return image_links
	
def count_numbs(string):
	digits = 0
	for i in string:
		if i.isdigit():
			digits += 1
	if digits >= 7:
		return True
	else:
		return False
	
def filter_links(link_ls):
	images = [x for x in link_ls if "node" in x]
	images = [x for x in images if "/bgimage" in x]
	images = [x for x in images if "https" in x]
	images = [x for x in images if "from" not in x]
	images = [x for x in images if count_numbs(x) == True]
	return images
	
def image_page_finder():
	image_links =[]
	for i in range(0, 505, 24):
		raw_text = call_web(i)
		page_links = extract_image_links(raw_text)
		page_photo_links = filter_links(page_links)
		image_links.extend(page_photo_links)
		time.sleep(1) # A lot of websites detect bots based on how fast they are called in a row. 
	return image_links
	
def image_finder(page_ls):
	image_pages = []
	image_links = []
	for i in page_ls:
		image_pages.append(call_image_page(i))
		time.sleep(1) # At some point, calling a website too often is bad. 
	for i in image_pages:
		image_links.extend(extract_central_image_link(i))
	image_links = [x for x in image_links if "jpg" in x]
	return image_links
		
	
def image_downloader(image_ls):
	for i in image_ls:
		try:
			img_data = req.get(i).content
			img_name = os.path.basename(i)
			with open(os.path.join(impath, img_name), "wb") as f:
				f.write(img_data)
			time.sleep(1) # Once again, I don't want to go over my alloted requests. 
		except Exception as e:
			print(e)

# Run Application

if __name__=="__main__":
	image_page_links = list(set(image_page_finder()))
	print(len(image_page_links))
	image_links = image_finder(image_page_links)
	print(len(image_links)) # How many potential images does this return? Ideally I want 100-200 or more.
#	As it currently stands, this is just over 2K images... prior to being sorted and any other cleaning.
#	image_downloader(image_links) #Use in Prod Only
	