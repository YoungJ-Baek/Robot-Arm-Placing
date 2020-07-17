import cv2
import numpy as np
import os

dir_path="/home/youngj/Desktop/FPCB_Image/Grab_Rigid3/"

img_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
img_files.sort()
num_of_imgs = img_files.__len__()

ref=cv2.imread('remove_tool.png')
ref=cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

for i in range(0, num_of_imgs):
	img_name = img_files[i]
	img_path = dir_path + img_name
	img = cv2.imread(img_path)

	ver_size, hor_size = img.shape[:2]
	img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	for x in range(0,hor_size):
		for y in range(0, ver_size):
			if ref[y][x]==255:
				img_gray[y][x]=0

	cv2.imwrite('remove_tool_'+img_name, img_gray)
