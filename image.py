'''
import sys
sys.path.append("/media/saumil/Extra_Linux/818B/blender_depth")
from image import *
'''
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

def delete_cube():
	bpy.ops.object.select_all(action='DESELECT')
	# bpy.data.objects['Camera'].select = True    # Blender 2.7x
	bpy.data.objects['Cube'].select_set(True) # Blender 2.8x
	bpy.ops.object.delete() 

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
	# path_dir = "/media/saumil/Extra_Linux/" #save for restore
	nodes = bpy.context.scene.node_tree.nodes
	os.mkdir(path_dir+str(i)+"/")
	for cam in [obj for obj in bpy.data.objects if obj.type == 'CAMERA']:
	    bpy.context.scene.camera = cam
	    bpy.context.scene.render.filepath = os.path.join(path_dir +str(i)+"/", cam.name)
	    nodes['File Output'].base_path = path_dir + str(i) + "/" 
	    bpy.ops.render.render(write_still=True)
	    bpy.context.scene.render.filepath = path_dir + str(i)+"/"

def assign_material(image_path, ob):
	mat = bpy.data.materials.new(name=ob.name+"_material")
	mat.use_nodes = True
	bsdf = mat.node_tree.nodes["Principled BSDF"]
	texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
	texImage.image = bpy.data.images.load(image_path)
	mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
	# Assign it to object
	if ob.data.materials:
	    ob.data.materials[0] = mat
	else:
	    ob.data.materials.append(mat)

def createWalls(wallDirectory):
	images = glob.glob(wallDirectory+"/*")
	locations = [Vector((  0, 10,  5)), 
				 Vector(( 10,  0,  5)), 
				 Vector((  0,-10,  5)), 
				 Vector((-10,  0,  5)),
				 Vector((  0,  0,  0)),
				 Vector((  0,  0, 10))]
	orientations = [Vector((0, 0, 0))]*6
	scales = [Vector((  10, 0.01,    5)), 
	   		  Vector((0.01,   10,    5)), 
	   		  Vector((  10, 0.01,    5)), 
	   		  Vector((0.01,   10,    5)),
	   		  Vector((  10,   10, 0.01)),
	   		  Vector((  10,   10, 0.01))]
	for i in range(6):
		image_index = random.randint(0, len(images)-1)
		wall_name = "Wall_" + str(i)
		print("Image index: ", image_index, " number of images: ", len(images))
		bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
		bpy.data.objects['Cube.001'].name = wall_name
		bpy.data.objects[wall_name].location = locations[i]
		bpy.data.objects[wall_name].rotation_euler = orientations[i]
		bpy.data.objects[wall_name].scale = scales[i]
		assign_material(images[image_index], bpy.data.objects[wall_name])

def addRandomMeshes(textures, n):
	l = ["Cylinder", "Cone", "Cube", "Torus", "Sphere"]
	for i in range(n):
		name = l[random.randint(0, len(l)-1)]
		search_name = name+".001"
		new_name = "a_" + str(i)
		print("Object selected is - ", name, " New name - ", new_name)
		if name == "Cylinder":
			bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
		if name == "Cone":
			bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
		if name == "Torus":
			bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)
		if name == "Sphere":
			bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))			
		if name == "Cube":
			bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
	imp_names = []
	for na in bpy.data.objects:
		initial = na.name[0]
		if initial in ['C','T','S'] and na.name != "Camera":
			assign_material(textures[random.randint(0, len(textures)-1)], na)
	# assign_material(textures[random.randint(0, len(textures)-1)], bpy.data.objects[search_name])
		# bpy.data.objects[search_name].name = new_name	
	pass

def preadd():
	bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
	bpy.ops.mesh.primitive_cone_add(radius1=1, radius2=0, depth=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
	bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)
	bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
	pass

def delete_pre():
	l = ["Cylinder", "Cone", "Cube", "Torus", "Sphere"]
	for ll in l:
		bpy.ops.object.select_all(action='DESELECT')
		bpy.data.objects[ll].select_set(True) # Blender 2.8x
		bpy.ops.object.delete()
	pass

def getdata(start=0):
	location1_start = Vector((10,-8,5))
	offset = 0
	height = 5
	rotations = [Euler((1.57, 0, 1.57), 'XYZ'),
				 Euler((1.57, 0, -1.57), 'XYZ'),
				 Euler((1.57, 0, 1.57*2), 'XYZ'),
				 Euler((1.57, 0, 0), 'XYZ')]
	bpy.data.objects['Camera'].location = location1_start
	y_locations = np.arange(-8, 8, 0.1)
	j = start
	for i in y_locations:
		bpy.data.objects['Camera'].rotation_euler = rotations[0]
		bpy.data.objects['Camera'].location = Vector((offset, i, height))
		render_and_save(save_directory, j)
		j+=1
		bpy.data.objects['Camera'].rotation_euler = rotations[1]
		bpy.data.objects['Camera'].location = Vector((-offset, i, height))
		render_and_save(save_directory, j)
		j+=1
		bpy.data.objects['Camera'].rotation_euler = rotations[2]
		bpy.data.objects['Camera'].location = Vector((i, offset, height))
		render_and_save(save_directory, j)
		j+=1
		bpy.data.objects['Camera'].rotation_euler = rotations[3]
		bpy.data.objects['Camera'].location = Vector((i,-offset, height))
		render_and_save(save_directory, j)
		j+=1
		print(str(j), " images saved")

wall_directory = "/media/saumil/Extra_Linux/818B/blender_depth/walls"
save_directory = "/media/saumil/Extra_Linux/818B/blender_depth/data/"
textures = "/media/saumil/Extra_Linux/818B/blender_depth/textures/*"

bpy.context.scene.render.resolution_x = 256
bpy.context.scene.render.resolution_y = 256

available_textures = glob.glob(textures)
createWalls(wall_directory)
set_nodes()
connect_nodes()

preadd()
addRandomMeshes(available_textures, 14)
delete_pre()

# render_and_save(save_directory, 1)

new_location = Vector((10,-10,5))
bpy.data.objects['Camera'].location = new_location
# render_and_save(save_directory, 2)

