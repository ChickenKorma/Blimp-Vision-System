# ------------------------------------------ MODULES ------------------------------------------


import cv2 as cv
import numpy as np


# ------------------------------------------ VARIABLES ------------------------------------------


data_path_prefix = "D:/Uni Stuff/IP/Data/"
image_path_prefix = data_path_prefix + "Chequerboard Images/image_"

chequerboard_length = 7
chequerboard_width = 7

total_images = 20

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

# Returns a string of whitespace seperated elements of a matrix
def matrix_to_string(matrix):
    result = ""

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            result += " " + str(matrix[i, j])

    return result


# ------------------------------------------ MAIN ------------------------------------------


for image_no in range(total_images):
    image = cv.imread(image_path_prefix + str(image_no) + ".png")
    find_corners(image)

ret, camera_matrix, distortion_coeffs, rot_vecs, trans_vecs = cv.calibrateCamera(obj_points, image_points, (res_width, res_height), None, None)

new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (res_width, res_height), 1, (res_width, res_height))

with open(data_path_prefix + "Camera Properties.txt", 'w', encoding='UTF8', newline='') as camera_properties_txt:
    camera_properties_txt.write("camera_matrix:" + matrix_to_string(camera_matrix) + "\n")
    camera_properties_txt.write("distortion_coeffs:" + matrix_to_string(distortion_coeffs) + "\n")
    camera_properties_txt.write("new_camera_matrix:" + matrix_to_string(new_camera_matrix))