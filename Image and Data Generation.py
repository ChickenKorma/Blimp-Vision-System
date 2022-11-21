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
        
# Generates and returns a new random position vector within 'max_distance' to the origin and with a z offset of 'height_offset'
def new_object_position(max_distance, height_offset):
    x_pos = (random.random() - 0.5) * 2 * max_distance
    y_pos = (random.random() - 0.5) * 2 * max_distance
    z_pos = ((random.random() - 0.5) * 2 * max_distance) + height_offset
    
    return mathutils.Vector((x_pos, y_pos, z_pos))

# Generates and returns a new random euler rotation
def new_object_rotation():
    x_rot = (random.random() - 0.5) * 2 * math.pi
    y_rot = (random.random() - 0.5) * 2 * math.pi
    z_rot = (random.random() - 0.5) * 2 * math.pi
    
    return mathutils.Euler((x_rot, y_rot, z_rot))

# Generates and returns a new camera pose
# Position is on a circle of radius 'distance' with a random angle to the x axis and a fixed z position
# Rotation points towards the origin with fixed pitch and no roll angles
def new_camera_pose(distance):
    angle = random.random() * 2 * math.pi
    
    x_pos = distance * math.cos(angle)
    y_pos = distance * math.sin(angle)   
    position = mathutils.Vector((x_pos, y_pos, 0.5))
    
    z_rot = (math.pi / 2) + angle
    rotation = mathutils.Euler((math.radians(106), 0, z_rot))
    
    return position, rotation

# Finds and returns the position and rotation of 'object' as a list of strings of each axis
def get_pose_data(object):
    pos_x = str(object.location.x)
    pos_y = str(object.location.y)
    pos_z = str(object.location.z)

    rot_x = str(object.rotation_euler.x)
    rot_y = str(object.rotation_euler.y)
    rot_z = str(object.rotation_euler.z)

    return [pos_x, pos_y, pos_z, rot_x, rot_y, rot_z]

# Finds and returns the screen-space coordinates of the 2D bounding box of 'object'
def get_bounding_box(object, camera):
    object_matrix = object.matrix_world
    vertices = object.data.vertices
    
    res_width = bpy.context.scene.render.resolution_x
    res_height = bpy.context.scene.render.resolution_y
    
    vertex_screen_positions = np.empty([len(vertices), 2])
    
    i = 0
    
    while i < len(vertices):
        vertex_world_pos = object_matrix @ vertices[i].co
        
        vertex_relative_screen_pos = bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, camera, vertex_world_pos)
        
        vertex_screen_positions[i] = [vertex_relative_screen_pos[0] * res_width, res_height - (vertex_relative_screen_pos[1] * res_height)]
        
        i += 1
        
    min = vertex_screen_positions.min(axis=0)
    max = vertex_screen_positions.max(axis=0)
    
    return [math.floor(min[0]), math.floor(min[1]), math.ceil(max[0]), math.ceil(max[1])]    

blimp_object = bpy.data.objects["Blimp"]
camera_object = bpy.data.objects["Camera"]

image_path_prefix = "D:/Uni Stuff/IP/Data/Images/sphere_cube_"

total_images = 10
image_no = 0

csv_path_prefix = "D:/Uni Stuff/IP/Data/CSVs/"
csv_pose_header = ["pos_x", "pos_y", "pos_z", "rot_x", "rot_y", "rot_z"]
csv_bbox_header = ["min_x", "min_y", "max_x", "max_y"]

with open(csv_path_prefix + "blimp poses.csv", 'w', encoding='UTF8', newline='') as blimp_csv, open(csv_path_prefix + "camera poses.csv", 'w', encoding='UTF8', newline='') as camera_csv, open(csv_path_prefix + "boundary boxes.csv", 'w', encoding='UTF8', newline='') as bbox_csv:
    blimp_writer = csv.writer(blimp_csv)
    blimp_writer.writerow(csv_pose_header)

    camera_writer = csv.writer(camera_csv)
    camera_writer.writerow(csv_pose_header)
    
    bbox_writer = csv.writer(bbox_csv)
    bbox_writer.writerow(csv_bbox_header)

    while image_no < total_images: 
        blimp_object.location = new_object_position(5, 6)
        blimp_object.rotation_euler = new_object_rotation()
        
        camera_object.location, camera_object.rotation_euler = new_camera_pose(40)
        
        # Redraw scene, not advised by Blender but is necessary to update objects and camera for the new render
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        bpy.context.scene.render.filepath = image_path_prefix + str(image_no) + ".png"
        bpy.ops.render.render(write_still = 1)

        blimp_writer.writerow(get_pose_data(blimp_object))
        camera_writer.writerow(get_pose_data(camera_object))
        
        bbox_writer.writerow(get_bounding_box(blimp_object, camera_object))
        
        image_no += 1   