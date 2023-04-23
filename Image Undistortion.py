# ------------------------------------------ MODULES ------------------------------------------


import cv2 as cv
import numpy as np
import time


# ------------------------------------------ VARIABLES ------------------------------------------


data_path_prefix = "D:/Uni Stuff/IP/Data/"
raw_image_path_prefix = data_path_prefix + "Blimp Images/Raw/image_"
corrected_image_path_prefix = data_path_prefix + "Blimp Images/Corrected/image_"
bbox_path_prefix = data_path_prefix + "Bounding Boxes/image_"

total_images = 5

res_width = 1920
res_height = 1080


# ------------------------------------------ MAIN ------------------------------------------

loaded_arrays = np.load(data_path_prefix + "Camera Properties.npz", allow_pickle=True)

camera_matrix = loaded_arrays['camera_matrix']
distortion_coeffs = loaded_arrays['distortion_coeffs']
new_camera_matrix = loaded_arrays['new_camera_matrix']

correction_times = np.array([])

for image_no in range(total_images):
    start_time = time.time()

    image = cv.imread(raw_image_path_prefix + str(image_no) + ".png")

    undistorted_image = cv.undistort(image, camera_matrix, distortion_coeffs, None, new_camera_matrix)

    with open(bbox_path_prefix + str(image_no) + ".txt", 'r', encoding='UTF8') as bbox_txt:
        bbox_data = bbox_txt.read().split()
        
    bbox_center_x = float(bbox_data[1]) * res_width
    bbox_center_y = float(bbox_data[2]) * res_height
    bbox_width = float(bbox_data[3]) * res_width
    bbox_height = float(bbox_data[4]) * res_height

    min_x = bbox_center_x - (0.5 * bbox_width)
    min_y = bbox_center_y - (0.5 * bbox_height)

    max_x = bbox_center_x + (0.5 * bbox_width)
    max_y = bbox_center_y + (0.5 * bbox_height)

    points = np.array([[min_x, min_y], [min_x, max_y], [max_x, min_y], [max_x, max_y]])
    undistorted_points = cv.undistortPoints(points, camera_matrix, distortion_coeffs, P=new_camera_matrix)

    new_min = undistorted_points.min(axis=0) 
    new_max = undistorted_points.max(axis=0)

    new_min_x = int(new_min[0][0])
    new_min_y = int(new_min[0][1])
    new_max_x = int(new_max[0][0])
    new_max_y = int(new_max[0][1])

    min_x = int(min_x)
    min_y = int(min_y)
    max_x = int(max_x)
    max_y = int(max_y)

    end_time = time.time()
    correction_times = np.append(correction_times, [end_time - start_time])

    #cv.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
    cv.rectangle(undistorted_image, (min_x, min_y), (max_x, max_y), (0, 0, 255), 1)
    cv.rectangle(undistorted_image, (new_min_x, new_min_y), (new_max_x, new_max_y), (0, 255, 0), 1)

    #cv.imwrite(corrected_image_path_prefix + str(image_no) + ".png", undistorted_image)

    #cv.imshow("Raw", image)
    cv.imshow("Corrected", undistorted_image)

np.savez(data_path_prefix + "Correction Times.npz", correction_times = correction_times)

cv.waitKey(0)