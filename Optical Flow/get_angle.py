import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import math

def writeFlow(flow, fname):
	f = open(fname, 'wb')
	f.write('PIEH'.encode('utf-8'))
	np.array([flow.shape[1], flow.shape[0]], dtype=np.int32).tofile(f)
	flow = flow.astype(np.float32)
	flow.tofile(f)

try:
	if not(os.path.exists("temp")):
		os.makedirs(os.path.join("temp"))
except OSError as e:
	if e.errno !=errno.EEXIST:
		print("Failed to create directory!!!!!")
		raise


dir_img1=input("Input image1's directory: ")
dir_img2=input("Input image2's directory: ")
dir_result=input("Input result file's directory: ")

ref=cv2.imread(dir_img1)
ref=cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
rows, cols=ref.shape[:2]
print(rows)
print(cols)
if rows==720 and cols==1280:
	x=794
	y=640
	hor_crop_point = x - 150
	ver_crop_point = y - 150
	hor_crop_length = 300
	ver_crop_length = 300
	ref_crop = ref[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]
	cv2.imwrite(dir_img1, ref_crop)

ref=cv2.imread(dir_img2)
ref=cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
rows, cols=ref.shape[:2]
if rows==720 and cols==1280:
	x=794
	y=640
	hor_crop_point = x - 150
	ver_crop_point = y - 150
	hor_crop_length = 300
	ver_crop_length = 300
	ref_crop = ref[ver_crop_point: ver_crop_point + ver_crop_length, hor_crop_point: hor_crop_point + hor_crop_length]
	cv2.imwrite(dir_img2, ref_crop)

total_angle=0
same=False
direction=True
first=True

if os.listdir('temp'):
	os.remove("temp/temp.png")

while same==False:
	
	if not os.listdir('temp'):
		img1=cv2.imread(dir_img2)
		os.system("bash run-network.sh -n FlowNet2 -v " + dir_img1 + " " + dir_img2 + " " + dir_result)
	else:
		img1=cv2.imread("temp/temp.png")
		os.system("bash run-network.sh -n FlowNet2 -v " + dir_img1 + " temp/temp.png " + dir_result)

	#img=cv2.imread("data/RefCrop.png")
	img=cv2.imread("data/trans.png")
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	fname=dir_result
	f=open(fname, 'rb')

	header = f.read(4)
	if header.decode("utf-8") != 'PIEH':
		raise Exception('Flow file header does not contain PIEH')
	width = np.fromfile(f, np.int32, 1).squeeze()
	height = np.fromfile(f, np.int32, 1).squeeze()
	flow = np.fromfile(f, np.float32, width * height * 2).reshape((height, width, 2))

	vector_map=flow.astype(np.float32)
	zero_count=0

	for x in range(0, width):
		for y in range(0, height):
			if img[y][x]==0 :
				vector_map[y,x,0]=0
				vector_map[y,x,1]=0
				zero_count+=1

	writeFlow(vector_map, fname)

	data_ang=np.zeros(width*height-zero_count)
	fx_sum=0
	count=0
	max_angle=-999
	min_angle=999
	middle=[150,150]


	for x in range(0, width):
		for y in range(0, height):
			fx=vector_map[y,x,0]
			fy=vector_map[y,x,1]
			fx_sum+=fx
		
			vec1=[middle[0]-float(x), middle[1]-float(y)]
			vec2=[middle[0]-float(x)+float(fx), middle[1]-float(y)+float(fy)]
			mag1=math.sqrt(vec1[0]*vec1[0]+vec1[1]*vec1[1])
			mag2=math.sqrt(vec2[0]*vec2[0]+vec2[1]*vec2[1])
			if fx!=0 and fy!=0:
				try:
					angle = math.degrees(math.acos((vec1[0]*vec2[0]+vec1[1]*vec2[1])/(mag1*mag2)))
				except ValueError:
					angle = 0
				except ZeroDivisionError:
					angle=0
				if angle>max_angle:
					max_angle=angle
				if angle<min_angle:
					min_angle=angle
				data_ang[count]=angle
				count+=1

	bins=np.arange(min_angle, max_angle)
	bins=np.arange(1, 45)
	histogram=plt.hist(data_ang, bins)
	amount=histogram[0]
	rotangle=histogram[1]
	tall=0
	posx=0
	for j in range(0, len(amount)):
		if amount[j]>tall:
			tall=amount[j]
			posx=j
	print(rotangle[posx])
	
	total_angle+=rotangle[posx]

	if fx_sum/(width*height-zero_count)<0:
		if first==True:
			direction=True
		first=False
		rot = cv2.getRotationMatrix2D((middle[0],middle[1]), -rotangle[posx] , 1)
	else:
		if first==True:
			direction=False
		first=False
		rot = cv2.getRotationMatrix2D((middle[0],middle[1]), rotangle[posx] , 1)
	dst = cv2.warpAffine(img1, rot, (width, height))
	cv2.imwrite("temp/temp.png", dst)

	if rotangle[posx]<=2:
		same=True

if direction==True:
	print("direction: clockwise")
else:
	print("direction: counter-clockwise")
print("total angle:"+str(total_angle))
img=cv2.imread(dir_img2)
if direction==True:
	rot = cv2.getRotationMatrix2D((middle[0],middle[1]), -total_angle , 1)
else:
	rot = cv2.getRotationMatrix2D((middle[0],middle[1]), total_angle , 1)
dst = cv2.warpAffine(img, rot, (width, height))
cv2.imshow("img",dst)
cv2.waitKey(0)
cv2.imwrite("data/rot.png", dst)
