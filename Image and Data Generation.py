# ------------------------------------------ MODULES ------------------------------------------


# Blender modules
import bpy
import bpy_extras.object_utils

# Extra modules
import numpy as np

# Python modules
import math
import mathutils
import random
import csv


# ------------------------------------------ VARIABLES ------------------------------------------

# Images
total_images = 5

image_path_prefix = "D:/Uni Stuff/IP/Data/Images/sphere_cube_"

# Data
csv_path_prefix = "D:/Uni Stuff/IP/Data/CSVs/"
csv_pose_header = ["pos_x", "pos_y", "pos_z", "rot_x", "rot_y", "rot_z"]
csv_bbox_header = ["min_x", "min_y", "max_x", "max_y"]

# Blimp
min_distance = 5
max_distance = 75

# Camera
angle_of_view = 71.5


# ------------------------------------------ FIXED ------------------------------------------

# Objects
blimp_object = bpy.data.objects["Blimp"]
camera_object = bpy.data.objects["Camera"]

# Camera
aspect_ratio = bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y


# ------------------------------------------ FUNCTIONS ------------------------------------------


# Generates and returns a new random position vector within 'max_distance' to the origin and with a z offset of 'height_offset'
def new_blimp_position():  
    x_pos = min_distance + ((max_distance - min_distance) * random.random())

    max_y = x_pos * math.tan(math.radians(0.5 * angle_of_view))
    y_pos = (random.random() - 0.5) * 2 * max_y

    max_z = max_y / aspect_ratio
    z_pos = (random.random() - 0.5) * 2 * max_z
    
    return mathutils.Vector((x_pos, y_pos, z_pos))

# Generates and returns a new random euler rotation
def new_blimp_rotation():
    roll = (random.random() - 0.5) * 2 * math.pi

    pitch = (random.random() - 0.5) * 2 * math.pi

    yaw = (random.random() - 0.5) * 2 * math.pi
    
    return mathutils.Euler((roll, pitch, yaw))

# Finds and returns the position and rotation of 'object' as a list of strings of each axis
def get_blimp_pose():
    pos_x = str(blimp_object.location.x)
    pos_y = str(blimp_object.location.y)
    pos_z = str(blimp_object.location.z)

    rot_x = str(blimp_object.rotation_euler.x)
    rot_y = str(blimp_object.rotation_euler.y)
    rot_z = str(blimp_object.rotation_euler.z)

    return [pos_x, pos_y, pos_z, rot_x, rot_y, rot_z]

# Finds and returns the screen-space coordinates of the 2D bounding box of 'object'
def get_blimp_bounding_box():
    blimp_matrix = blimp_object.matrix_world
    vertices = blimp_object.data.vertices
    
    res_width = bpy.context.scene.render.resolution_x
    res_height = bpy.context.scene.render.resolution_y
    
    vertex_screen_positions = np.empty([len(vertices), 2])
    
    i = 0
    
    while i < len(vertices):
        vertex_world_pos = blimp_matrix @ vertices[i].co
        
        vertex_relative_screen_pos = bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, camera_object, vertex_world_pos)
        
        vertex_screen_positions[i] = [vertex_relative_screen_pos[0] * res_width, res_height - (vertex_relative_screen_pos[1] * res_height)]
        
        i += 1
        
    min = vertex_screen_positions.min(axis=0)
    max = vertex_screen_positions.max(axis=0)
    
    return [math.floor(min[0]), math.floor(min[1]), math.ceil(max[0]), math.ceil(max[1])]    


# ------------------------------------------ MAIN ------------------------------------------


with open(csv_path_prefix + "blimp poses.csv", 'w', encoding='UTF8', newline='') as blimp_csv, open(csv_path_prefix + "boundary boxes.csv", 'w', encoding='UTF8', newline='') as bbox_csv:
    blimp_writer = csv.writer(blimp_csv)
    blimp_writer.writerow(csv_pose_header)
    
    bbox_writer = csv.writer(bbox_csv)
    bbox_writer.writerow(csv_bbox_header)

    image_no = 0

    while image_no < total_images: 
        blimp_object.location = new_blimp_position()
        blimp_object.rotation_euler = new_blimp_rotation()
        
        # Redraw scene, not advised by Blender but is necessary to update objects and camera for the new render
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        bpy.context.scene.render.filepath = image_path_prefix + str(image_no) + ".png"
        bpy.ops.render.render(write_still = 1)

        #blimp_writer.writerow(get_blimp_pose())
        
        #bbox_writer.writerow(get_blimp_bounding_box())
        
        image_no += 1   