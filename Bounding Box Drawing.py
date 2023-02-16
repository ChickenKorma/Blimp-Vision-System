import cv2 as cv
import csv

bbox_path_prefix = "D:/Uni Stuff/IP/Data/Bounding Boxes/bbox_"
img_path_prefix = "D:/Uni Stuff/IP/Data/Images/image_"

no_images = 5

res_width = 1920
res_height = 1080

for image_no in range(no_images):
    with open(bbox_path_prefix + str(image_no) + ".txt", 'r', encoding='UTF8') as bbox_txt:
        bbox_data = bbox_txt.read().split()
        
        bbox_center_x = float(bbox_data[1]) * res_width
        bbox_center_y = float(bbox_data[2]) * res_height
        bbox_width = float(bbox_data[3]) * res_width
        bbox_height = float(bbox_data[4]) * res_height

        min_x = int(bbox_center_x - (0.5 * bbox_width))
        min_y = int(bbox_center_y - (0.5 * bbox_height))

        max_x = int(bbox_center_x + (0.5 * bbox_width))
        max_y = int(bbox_center_y + (0.5 * bbox_height))

        img = cv.imread(img_path_prefix + str(image_no) + ".png")

        cv.rectangle(img, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
        cv.imshow("Bounding box of image " + str(image_no), img)

cv.waitKey(0)