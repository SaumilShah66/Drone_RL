import bpy,sys

import glob
import random
from object_print3d_utils import (
    mesh_helpers,
    report,
)
import bmesh
from mathutils import *
import os
import numpy as np
from blender_utils import *
from exr2png import exr2numpy

def render_and_save_(path_dir):
	nodes = bpy.context.scene.node_tree.nodes
	if not os.path.isdir(path_dir):
		os.mkdir(path_dir)
	for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
	    bpy.context.scene.camera = cam
	    bpy.context.scene.render.filepath = path_dir
	    nodes['File Output'].base_path = path_dir 
	    bpy.ops.render.render(write_still=True)
	    bpy.context.scene.render.filepath = path_dir

class Environment():
	def __init__(self, cam, initial_position, initial_orientation, dir, rotation_step=30,
				 forward_step = 0.5):
		self.cam =cam
		self.count=0
		self.initial_position = initial_position
		self.initial_orientation = initial_orientation
		self.root_dir = dir
		self.rotation_step = np.radians(rotation_step)
		self.forward_step = forward_step
		self.episode = 0
		self.pi = np.radians(90)
		self.current_image = None
		self.current_depth_numpy = None
		self.threshold = 0.01 # Meters

	def step(self, action):
		## 0 -- Left || 1 -- Right || 2 -- Forward
		self.take_action(action)
		directory = self.root_dir + "/Episode_" + str(self.episode)
		render_and_save_(directory)
		self.current_image = cv2.imread(directory+"/Camera.png")
		self.current_depth_numpy = exr2numpy(directory+"/Image0001.exr", maxvalue=100, normalize=False)
		pass

	def checkCollision(self):
		minimum_depth = self.current_depth_numpy.min()
		if minimum_depth <= self.threshold:
			return True
		else:
			return False

	def updateEpisode(self):
		self.episode += 1

	def take_action(self, action):
		## 0 -- Left || 1 -- Right || 2 -- Forward
		old_yaw = self.cam.rotation_euler.z
		if action==0:
			self.cam.rotation_euler.z -= self.rotation_step
		if action==1:
			self.cam.rotation_euler.z += self.rotation_step
		if action==2:
			self.cam.location.x += self.forward_step*np.cos(self.pi + self.cam.rotation_euler.z)
			self.cam.location.y += self.forward_step*np.sin(self.pi + self.cam.rotation_euler.z)
		
	def reset(self):
		self.count = 0
		self.initial_position = initial_position
		self.initial_orientation = initial_orientation
		self.cam.location = self.initial_position
		self.cam.rotation_euler = self.initial_orientation
		pass