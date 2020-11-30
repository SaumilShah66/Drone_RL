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
import cv2

def render_and_save_(path_dir):
	nodes = bpy.context.scene.node_tree.nodes
	if not os.path.isdir(path_dir):
		os.mkdir(path_dir)
	for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
	    bpy.context.scene.camera = cam
	    bpy.context.scene.render.filepath = path_dir + "/Camera.png"
	    nodes['File Output'].base_path = path_dir 
	    bpy.ops.render.render(write_still=True)
	    # bpy.context.scene.render.filepath = path_dir

class Environment():
	def __init__(self, initial_position = Vector((0,0,5)), initial_orientation = Euler((1.57,0,0),'XYZ'),
				 root_dir = "/home/saumil/RL_exp", rotation_step=30, forward_step = 0.5):
		self.cam = bpy.data.objects['Camera']
		self.count=0
		self.initial_position = initial_position
		self.initial_orientation = initial_orientation
		if not os.path.isdir(root_dir):
			os.mkdir(root_dir)
		self.root_dir = root_dir
		self.rotation_step = np.radians(rotation_step)
		self.forward_step = forward_step
		self.episode = 0
		self.pi = np.radians(90)
		self.current_image = None
		self.current_depth_numpy = None
		self.threshold = 0.01 # Meters
		self.previous_actions = [2,2,2,2]
		
	def step(self, action):
		## 0 -- Left || 1 -- Right || 2 -- Forward
		self.count += 1
		self.previous_actions.remove(self.previous_actions[0])
		self.previous_actions.append(action)
		self.take_action(action)
		directory = self.root_dir + "/Episode_" + str(self.episode)
		render_and_save_(directory)
		self.current_image = cv2.imread(directory+"/Camera.png")
		self.current_depth_numpy = exr2numpy(directory+"/Image0001.exr", maxvalue=100, normalize=False)
		reward = self.calculate_reward()
		collide = self.checkCollision()
		if collide:
			reward=-10
		return self.current_image, reward, collide

	def calculate_reward(self):
		if not 2 in self.previous_actions:
			reward = -1
		else:
			reward = 1
		return reward

	def checkCollision(self):
		x, y, z = self.cam.location.x, self.cam.location.y, self.cam.location.z 
		if x >=10 or x<=-10: 
			os.system("echo outside x")
			return True
		if x >=10 or x<=-10: 
			os.system("echo outside y")
			return True
		minimum_depth = self.current_depth_numpy.min()
		if minimum_depth <= self.threshold:
			os.system("echo Collided %s"%minimum_depth)
			return True
		else:
			os.system("echo Not collided %s"%minimum_depth)
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
		self.cam.location = self.initial_position
		self.cam.rotation_euler = self.initial_orientation
		directory = self.root_dir + "/Episode_" + str(self.episode)
		render_and_save_(directory)
		self.current_image = cv2.imread(directory+"/Camera.png")
		self.current_depth_numpy = exr2numpy(directory+"/Image0001.exr", maxvalue=100, normalize=False)
		self.updateEpisode()
		return self.current_image