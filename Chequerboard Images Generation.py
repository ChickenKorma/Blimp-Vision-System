# ------------------------------------------ MODULES ------------------------------------------


import bpy
import random
import mathutils
import math


# ------------------------------------------ VARIABLES ------------------------------------------


image_path_prefix = "D:/Uni Stuff/IP/Data/Chequerboard Images/image_"

total_images = 20

nominal_distance = 2.3
distance_variation = 0.5

max_off_angle = 35

chequerboard_obj = bpy.data.objects["Chequerboard"]


# ------------------------------------------ FIXED ------------------------------------------


# ------------------------------------------ FUNCTIONS ------------------------------------------


def new_chequerboard_position():
    x_pos = nominal_distance + ((random.random() - 0.5) * 2 * distance_variation)
    y_pos = 0
    z_pos = 0

    return mathutils.Vector((x_pos, y_pos, z_pos))

def new_chequerboard_rotation():
    x_rot = (random.random() - 0.5) * 2 * math.pi
    y_rot = (random.random() - 0.5) * 2 * math.radians(max_off_angle)
    z_rot = (random.random() - 0.5) * 2 * math.radians(max_off_angle)

    return mathutils.Euler((x_rot, y_rot, z_rot))


# ------------------------------------------ MAIN ------------------------------------------


for image_no in range(total_images):
    chequerboard_obj.location = new_chequerboard_position()
    chequerboard_obj.rotation_euler = new_chequerboard_rotation()

    # Redraw scene, not advised by Blender but is necessary to update objects and camera for the new render
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    bpy.context.scene.render.filepath = image_path_prefix + str(image_no) + ".png"
    bpy.ops.render.render(write_still = 1)