import cv2
import numpy as np 
import glob
from exr2png import exr2numpy

path = "data/"

folders = glob.glob(path + "*")
for i in range(len(folders)):
	img_name = path + str(i) + "/Camera.png"
	depth_name = path + str(i) + "/Image0001.exr"
	img = cv2.imread(img_name)
	depth = exr2numpy(depth_name, maxvalue=100, normalize=True)
	cv2.imshow('frame', img)
	cv2.imshow('Depth', depth)
	cv2.imwrite(path + str(i) + "/depth.png", depth)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cv2.destroyAllWindows()