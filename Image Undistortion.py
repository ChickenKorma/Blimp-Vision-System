# ------------------------------------------ MODULES ------------------------------------------


import cv2 as cv
import numpy as np


# ------------------------------------------ VARIABLES ------------------------------------------


data_path_prefix = "D:/Uni Stuff/IP/Data/"
raw_image_path_prefix = data_path_prefix + "Blimp Images/Raw/image_"
corrected_image_path_prefix = data_path_prefix + "Blimp Images/Corrected/image_"

total_images = 5


# ------------------------------------------ MAIN ------------------------------------------

loaded_arrays = np.load(data_path_prefix + "Camera Properties.npz", allow_pickle=True)

camera_matrix = loaded_arrays['camera_matrix']
distortion_coeffs = loaded_arrays['distortion_coeffs']
new_camera_matrix = loaded_arrays['new_camera_matrix']

for image_no in range(total_images):
    image = cv.imread(raw_image_path_prefix + str(image_no) + ".png")

    undistorted_image = cv.undistort(image, camera_matrix, distortion_coeffs, None, new_camera_matrix)

    cv.imwrite(corrected_image_path_prefix + str(image_no) + ".png", undistorted_image)