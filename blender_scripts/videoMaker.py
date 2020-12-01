import matplotlib.pyplot as plt 
import numpy as np 
try:
    import cv2
except:
    import sys
    sys.path.remove(sys.path[2])
    import cv2
import math
import argparse


Parser = argparse.ArgumentParser()
Parser.add_argument('--Video', default="../data/Tag0.mp4", help='Give path of the video')
Args = Parser.parse_args()
VideoPath = Args.Video

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
vw = cv2.VideoWriter("track.avi", fourcc, 30, (640,360))

# names = ["multipleTags.mp4","Tag0.mp4","Tag1.mp4","Tag2.mp4"]
cap = cv2.VideoCapture(VideoPath)
# names = ["multipleTags.mp4","Tag0.mp4","Tag1.mp4","Tag2.mp4"]

while (cap.isOpened()):	
	ret, frame = cap.read()
	vw.write(frame)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
vw.release()
cv2.destroyAllWindows()


