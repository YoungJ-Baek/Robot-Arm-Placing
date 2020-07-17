import cv2
import numpy as np

img1=cv2.imread("/home/youngj/fpcb_placement/DB_20200330_NonQR/Reference/0000.png")
img2=cv2.imread("/home/youngj/fpcb_placement/DB_20200330_NonQR/Reference/0002.png")
rows, cols = img1.shape[:2]

img1_gray=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray=cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

img_diff=img1_gray.copy()
img3_black=img1_gray.copy()
img3_white=img1_gray.copy()

for x in range(0,cols):
	for y in range(0, rows):
		if int(img1_gray[y][x])-int(img2_gray[y][x])<=15:
			img_diff[y][x]=0
		else:
			#img_diff[y][x]=int(img1_gray[y][x])-int(img2_gray[y][x])
			img_diff[y][x]=int(img1_gray[y][x])
			img3_black[y][x]=0
			img3_white[y][x]=255
img3=img_diff-img1_gray;


x = 794
y = 640
angle = 60
"""
hor_crop_point = 802 - 125
ver_crop_point = 657 - 125 
hor_crop_length = 250
ver_crop_length = 250
"""
hor_crop_point = x - 150
ver_crop_point = y - 150 
hor_crop_length = 300
ver_crop_length = 300
crop_x=x-hor_crop_point
crop_y=y-ver_crop_point

ref=img1_gray[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]
img1_crop = img_diff[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]
img3_black = img3_black[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]
img3_white = img3_white[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]

matrix = cv2.getRotationMatrix2D((crop_x, crop_y), angle, 1)
rot=cv2.warpAffine(img1_crop, matrix, (hor_crop_length, ver_crop_length))
cv2.imwrite("ref.png",ref)
cv2.imwrite("cropref.png",img1_crop)
cv2.imwrite("Img3_black.png", img3_black)
cv2.imwrite("Img3_white.png", img3_white)

background=img2_gray-img_diff
"""
cv2.imshow("img1", img1_gray)
cv2.imshow("img2.2", img3)
#cv2.imshow("crop", img1_crop)
#cv2.imshow("rot", rot)
cv2.imshow("img2.1", img_diff)
cv2.waitKey(0)
"""
