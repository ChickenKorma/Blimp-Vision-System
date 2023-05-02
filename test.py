import numpy as np
import cv2 as cv

data_path_prefix = "D:/Uni Stuff/IP/Data/"
img_path = data_path_prefix + "Blimp Images/Raw/image_0.png"

loaded_arrays = np.load(data_path_prefix + "Camera Properties.npz", allow_pickle=True)

camera_matrix = loaded_arrays['camera_matrix']
distortion_coeffs = loaded_arrays['distortion_coeffs'] 
new_camera_matrix = loaded_arrays['new_camera_matrix'] 

image = cv.imread(img_path)
undistorted_image = cv.undistort(image, camera_matrix, distortion_coeffs, None)
cv.imshow("_", undistorted_image)
cv.waitKey(0)