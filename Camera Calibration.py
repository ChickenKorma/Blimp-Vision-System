# ------------------------------------------ MODULES ------------------------------------------


import cv2 as cv
import numpy as np


# ------------------------------------------ VARIABLES ------------------------------------------


data_path_prefix = "D:/Uni Stuff/IP/Data/"
image_path_prefix = data_path_prefix + "Chequerboard Images/image_"

chequerboard_length = 7
chequerboard_width = 7

total_images = 30

res_width = 1920
res_height = 1080


# ------------------------------------------ FIXED ------------------------------------------


objp = np.zeros((chequerboard_length * chequerboard_width, 3), np.float32)
objp[:,:2] = np.mgrid[0:chequerboard_width, 0:chequerboard_length].T.reshape(-1,2)

obj_points = []
image_points = []

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# ------------------------------------------ FUNCTIONS ------------------------------------------


# Finds and stores the 3D and 2D locations of the chequerboard square corners
def find_corners(image):
    grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(grey_image, (chequerboard_width, chequerboard_length), None)

    if ret == True:
        obj_points.append(objp)
        corners2 = cv.cornerSubPix(grey_image, corners, (11,11), (-1,-1), criteria)
        image_points.append(corners2)


# ------------------------------------------ MAIN ------------------------------------------


for image_no in range(total_images):
    image = cv.imread(image_path_prefix + str(image_no) + ".png")
    find_corners(image)

ret, camera_matrix, distortion_coeffs, rot_vecs, trans_vecs = cv.calibrateCamera(obj_points, image_points, (res_width, res_height), None, None)
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (res_width, res_height), 1, (res_width, res_height))

print(camera_matrix)
print(new_camera_matrix)
print(distortion_coeffs)

np.savez(data_path_prefix + "Camera Properties.npz", camera_matrix=camera_matrix, distortion_coeffs=distortion_coeffs, new_camera_matrix=new_camera_matrix)