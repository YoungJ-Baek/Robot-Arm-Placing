from skimage.measure import compare_ssim
import cv2
import os

fdir="RefImages/"
img_list=os.listdir(fdir)

"""remove tool"""
remove_tool=cv2.imread('remove_tool.png')
remove_tool = cv2.cvtColor(remove_tool, cv2.COLOR_BGR2GRAY)
rows, cols = remove_tool.shape[:2]

for i in range(0, len(img_list)):
    img=cv2.imread(fdir+img_list[i])#rotated
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    for y in range(0,rows):
        for x in range(0,cols):
            if remove_tool[y][x]==255:
                img[y][x]=0

    cv2.imwrite(fdir+img_list[i], img)

"""get rotation center x, y"""
ref=cv2.imread(fdir+'0000_angle_0.000.png')#ref
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref_crop=ref[450:620,600:900]
height_crop,width_crop=ref_crop.shape[:2]

diff_map=ref_crop.copy()
sub=ref_crop.copy()

for i in range(1, len(img_list)):
    img=cv2.imread(fdir+img_list[i])#rotated
    img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if '-' in img_list[i]:
        angle=float(img_list[i][11:17])
    else:
        angle=float(img_list[i][11:16])

    height, width=ref.shape[:2]

    """SSIM Algorithm"""

    max_score=0
    center_x=0
    center_y=0

    for y in range(640-50,630+50):
        for x in range(794-50,794+50):

            matrix=cv2.getRotationMatrix2D((x,y),angle,1)
            dst=cv2.warpAffine(img,matrix,(width,height))

            dst_crop=dst[450:620,600:900]

            (score,diff)=compare_ssim(ref_crop,dst_crop,full=True)

            if score>max_score:
                max_score=score
                center_x=x
                center_y=y
                diff_map=(diff*255).astype("uint8")
                sub=ref_crop-dst_crop

    print("result of %s" % img_list[i])
    print("position : (%d, %d), \tscore : %f" %(center_x, center_y, max_score))
    # cv2.imshow('ref',ref_crop)
    # cv2.imshow('diff',diff_map)
    # cv2.imshow('sub',sub)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
