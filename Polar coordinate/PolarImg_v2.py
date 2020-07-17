import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import register_translation
from skimage.transform import warp_polar, rotate
from skimage.util import img_as_float
import cv2

radius = 300

theta=10

dir_path = "/home/youngj/Desktop/FPCB_Image/Grab_Rigid2/Remove_Tool/Crop_Img2/"

#img_name="RefImg.png"
img_name="trans.png"
img_path = dir_path + img_name
RefPCBImg=cv2.imread(img_path)
img1_gray=cv2.cvtColor(RefPCBImg, cv2.COLOR_BGR2GRAY)

height, width=img1_gray.shape[:2]

img1_gray=np.flipud(img1_gray)

img_name="RotImg.png"
img_path = dir_path + img_name
RotImg=cv2.imread(img_path)
img2_gray=cv2.cvtColor(RotImg, cv2.COLOR_BGR2GRAY)

img2_gray=np.flipud(img2_gray)

center_hor= 150
center_ver = 0

center = (center_ver, center_hor)

min_idx = 0
min_error = 10000
final_rotation = 0

rotated_polar = warp_polar(img2_gray, scaling='linear', center=center, radius=radius, multichannel=False)


center2 = (center_ver , center_hor)

image_polar = warp_polar(img1_gray, scaling='linear', center=center2, radius=radius, multichannel=False)
"""
for y in range(0, 360):
    if y >= 90-theta and y <= 90+theta:
        continue
    else:
        image_polar[y][:] = 0
"""
shifts, error, phasediff = register_translation(image_polar, rotated_polar)
print("Recovered value for counterclockwise rotation: {0}".format(shifts[0]))
print("error{0}".format(error))

fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.ravel()
ax[0].set_title("Original")
#ax[0].imshow(RefPCBImg)
ax[0].imshow(img1_gray)
ax[1].set_title("Rotated")
#ax[1].imshow(RotImg)
ax[1].imshow(img2_gray)
ax[2].set_title("Polar-Transformed Original")
ax[2].imshow(image_polar)
ax[3].set_title("Polar-Transformed Rotated")
ax[3].imshow(rotated_polar)
plt.savefig('flipud/fig_'+str(theta)+'_'+str(shifts[0])+'.png',dpi=300)
plt.imsave('flipud/flipud_ref.png',img1_gray)
plt.imsave('flipud/flipud_rot.png',img2_gray)
plt.imsave('flipud/'+str(theta)+'_image_polar.png',image_polar)
plt.imsave('flipud/'+str(theta)+'_rotated_polar.png',rotated_polar)

img1_gray=np.flipud(img1_gray)
matrix = cv2.getRotationMatrix2D((150, 150), shifts[0], 1)
img1_gray = cv2.warpAffine(img1_gray, matrix, (width, height))
img1_gray=np.flipud(img1_gray)
#plt.imsave('theta/'+str(theta)+'_'+str(shifts[0])+'_rotated.png',img1_gray)
plt.imsave('flipud/'+str(theta)+'_'+str(shifts[0])+'_rotated.png',img1_gray)

image_polar=warp_polar(img1_gray, scaling='linear', center=center2, radius=radius, multichannel=False)
diff=rotated_polar-image_polar
plt.imsave('flipud/diff.png',diff)
