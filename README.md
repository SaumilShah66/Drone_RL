# Drone_RL


Dataset can be downloaded from [here](https://drive.google.com/file/d/17eftRTyaoUpoCuT6tUdG9Ep9VsqYFm1M/view?usp=sharing).
Blender 2.91 was used to generate data.

Trained weights provided in 
$ results/last.hi5

import sys
sys.path.append("/media/saumil/Extra_Linux/818B/Drone_RL/blender_scripts")
from image import *
sys.path.append('/usr/lib/python3.7')
sys.path.append('/usr/lib/python3.7/lib-dynload')
sys.path.append('/home/saumil/.local/lib/python3.7/site-packages') 
sys.path.append('/usr/local/lib/python3.7/dist-packages')
sys.path.append('/usr/local/lib/python3.7/dist-packages/cv2')
sys.path.append('/usr/lib/python3/dist-packages')
from RL import *
run_rl()