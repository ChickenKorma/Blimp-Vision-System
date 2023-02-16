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


# Data
data_path_prefix = "D:/Uni Stuff/IP/Data/"
image_path_prefix = data_path_prefix + "Images/image_"
bbox_path_prefix = data_path_prefix + "Bounding Boxes/bbox_"

pose_header = ["pos_x", "pos_y", "pos_z", "rot_x", "rot_y", "rot_z"]

# Images
total_images = 5

# Blimp
min_distance = 5
max_distance = 75

# Camera
angle_of_view = 71.5


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
    roll = (random.random() - 0.5) * 2 * math.radians(10)

    pitch = (random.random() - 0.5) * 2 * math.radians(20)

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
        
        vertex_screen_positions[i] = [vertex_relative_screen_pos[0] * res_width, res_height - (vertex_relative_screen_pos[1] * res_height)]
        
        i += 1
        
    min = vertex_screen_positions.min(axis=0)
    max = vertex_screen_positions.max(axis=0)

    # YOLO bounding box format
    bbox_width = max[0] - min[0]
    bbox_height = max[1] - min[1]

    bbox_center_x = min[0] + (0.5 * bbox_width)
    bbox_center_y = min[1] + (0.5 * bbox_height)
    
    return [bbox_center_x / res_width, bbox_center_y / res_height, bbox_width / res_width, bbox_height / res_height]    


# ------------------------------------------ MAIN ------------------------------------------


with open(data_path_prefix + "blimp poses.csv", 'w', encoding='UTF8', newline='') as blimp_csv:
    blimp_writer = csv.writer(blimp_csv)
    blimp_writer.writerow(pose_header)

    image_no = 0

    while image_no < total_images: 
        blimp_object.location = new_blimp_position()
        blimp_object.rotation_euler = new_blimp_rotation()
        
        # Redraw scene, not advised by Blender but is necessary to update objects and camera for the new render
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        bpy.context.scene.render.filepath = image_path_prefix + str(image_no) + ".png"
        bpy.ops.render.render(write_still = 1)

        blimp_writer.writerow(get_blimp_pose())
        
        bbox_data = get_blimp_bounding_box()
        bbox_str = "0 " + str(bbox_data[0]) + " " + str(bbox_data[1]) + " " + str(bbox_data[2]) + " " + str(bbox_data[3])

        with open(bbox_path_prefix + str(image_no) + ".txt", 'w', encoding='UTF8') as bbox_txt:
            bbox_txt.write(bbox_str)
        
        image_no += 1   