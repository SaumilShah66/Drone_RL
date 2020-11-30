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


def set_nodes():
	# Setting Outfile node
	bpy.context.scene.use_nodes = True
	nodes = bpy.context.scene.node_tree.nodes
	outfile = nodes.new("CompositorNodeOutputFile")
	outfile.base_path = "Output path here"  ### Working
	bpy.data.scenes["Scene"].node_tree.nodes['File Output'].format.file_format = 'OPEN_EXR'
	outfile.layer_slots.new("Flow")

def connect_nodes():
	### Connect nodes
	##### https://devtalk.blender.org/t/how-to-connect-nodes-using-script-commands/11567
	node_tree = bpy.data.scenes["Scene"].node_tree
	dep = node_tree.nodes['Render Layers'].outputs['Depth']
	vec = node_tree.nodes['Render Layers'].outputs['Vector']
	dep2 = node_tree.nodes['File Output'].inputs[0]
	vec2 = node_tree.nodes['File Output'].inputs[1]
	node_tree.links.new(dep, dep2)
	node_tree.links.new(vec, vec2)

def render_and_save(path_dir, i):
	nodes = bpy.context.scene.node_tree.nodes
	os.mkdir(path_dir+str(i)+"/")
	for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
	    bpy.context.scene.camera = cam
	    bpy.context.scene.render.filepath = os.path.join(path_dir +str(i)+"/", cam.name)
	    nodes['File Output'].base_path = path_dir + str(i) + "/" 
	    bpy.ops.render.render(write_still=True)
	    bpy.context.scene.render.filepath = path_dir + str(i)+"/"