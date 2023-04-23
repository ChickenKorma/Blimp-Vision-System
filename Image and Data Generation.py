# ------------------------------------------ MODULES ------------------------------------------


# Blender modules
import bpy
import bpy_extras.object_utils

# Extra modules
import numpy as np
import cv2 as cv

# Python modules
import math
import mathutils
import random
import csv


# ------------------------------------------ VARIABLES ------------------------------------------


# Data
data_path_prefix = "D:/Uni Stuff/IP/Data/"
image_path_prefix = data_path_prefix + "Blimp Images/Raw/image_"
bbox_path_prefix = data_path_prefix + "Bounding Boxes/image_"
background_path_prefix = data_path_prefix + "Backgrounds/image_"

pose_header = ["pos_x", "pos_y", "pos_z", "rot_x", "rot_y", "rot_z"]
bbox_header = ["cent_x", "cent_y", "width", "height"]

# Images
total_images = 5
background_images = 3

# Blimp
min_distance = 5
max_distance = 76.5

max_pitch_angle = 45
max_roll_angle = 10

# Camera
angle_of_view = 68


# ------------------------------------------ FIXED ------------------------------------------

# Objects
blimp_object = bpy.data.objects["Blimp"]
camera_object = bpy.data.objects["Camera"]

# Blimp Data
blimp_vertices = blimp_object.data.vertices

# Camera Settings
res_width = bpy.context.scene.render.resolution_x
res_height = bpy.context.scene.render.resolution_y

aspect_ratio = res_width / res_height

#loaded_arrays = np.load(data_path_prefix + "Camera Properties.npz", allow_pickle=True)
#camera_matrix = loaded_arrays['camera_matrix']
#distortion_coeffs = loaded_arrays['distortion_coeffs']
#new_camera_matrix = loaded_arrays['new_camera_matrix']


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
    roll = (random.random() - 0.5) * 2 * math.radians(max_roll_angle)

    pitch = (random.random() - 0.5) * 2 * math.radians(max_pitch_angle)

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
    
    vertex_screen_positions = np.empty([len(blimp_vertices), 2])
    
    i = 0
    
    while i < len(blimp_vertices):
        vertex_world_pos = blimp_matrix @ blimp_vertices[i].co
        
        vertex_relative_screen_pos = bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, camera_object, vertex_world_pos)
        
        vertex_screen_positions[i] = [vertex_relative_screen_pos[0], 1 - vertex_relative_screen_pos[1]]
        
        i += 1
        
    min = vertex_screen_positions.min(axis=0)
    max = vertex_screen_positions.max(axis=0)

    min_x = min[0]
    max_x = max[0]
    min_y = min[1]
    max_y = max[1]

    # YOLO bounding box format
    bbox_width = max_x - min_x
    bbox_height = max_y - min_y

    bbox_center_x = min_x + (0.5 * bbox_width)
    bbox_center_y = min_y + (0.5 * bbox_height)
    
    return [bbox_center_x, bbox_center_y, bbox_width, bbox_height]    


# ------------------------------------------ MAIN ------------------------------------------


with open(data_path_prefix + "blimp poses.csv", 'w', encoding='UTF8', newline='') as blimp_csv, open(data_path_prefix + "bbox data.csv", 'w', encoding='UTF8', newline='') as bbox_csv:
    blimp_writer = csv.writer(blimp_csv)
    blimp_writer.writerow(pose_header)

    bbox_writer = csv.writer(bbox_csv)
    bbox_writer.writerow(bbox_header)

    background_no = -1

    for image_no in range(total_images): 
        blimp_object.location = new_blimp_position()
        blimp_object.rotation_euler = new_blimp_rotation()

        if background_no < background_images - 1:
            background_no += 1
        else:
            background_no = 0
            
        #bpy.context.scene.node_tree.nodes[4].image = bpy.data.images.load(background_path_prefix + str(background_no) + ".png")
        
        # Redraw scene, not advised by Blender but is necessary to update objects and camera for the new render
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        bpy.context.scene.render.filepath = image_path_prefix + str(image_no) + ".png"
        bpy.ops.render.render(write_still = 1)

        blimp_writer.writerow(get_blimp_pose())
        
        bbox_data = get_blimp_bounding_box()

        bbox_writer.writerow(bbox_data)

        bbox_str = "0 " + str(bbox_data[0]) + " " + str(bbox_data[1]) + " " + str(bbox_data[2]) + " " + str(bbox_data[3])

        with open(bbox_path_prefix + str(image_no) + ".txt", 'w', encoding='UTF8') as bbox_txt:
            bbox_txt.write(bbox_str)  