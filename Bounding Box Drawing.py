import cv2 as cv

image_no = 28

raw_bbox_path = "D:/Uni Stuff/IP/Data/Bounding Boxes/Raw/image_" + str(image_no) + ".txt"
raw_img_path = "D:/Uni Stuff/IP/Data/Blimp Images/Raw/image_" + str(image_no) + ".png"

corrected_bbox_path = "D:/Uni Stuff/IP/Data/Bounding Boxes/Corrected/image_" + str(image_no) + ".txt"
corrected_img_path = "D:/Uni Stuff/IP/Data/Blimp Images/Corrected/image_" + str(image_no) + ".png"

save_path = "D:/Uni Stuff/IP/Data/"

res_width = 1920
res_height = 1080

with open(raw_bbox_path, 'r', encoding='UTF8') as bbox_txt:
    bbox_data = bbox_txt.read().split()
    
    bbox_center_x = float(bbox_data[1]) * res_width
    bbox_center_y = float(bbox_data[2]) * res_height
    bbox_width = float(bbox_data[3]) * res_width
    bbox_height = float(bbox_data[4]) * res_height

    raw_min_x = int(bbox_center_x - (0.5 * bbox_width))
    raw_min_y = int(bbox_center_y - (0.5 * bbox_height))

    raw_max_x = int(bbox_center_x + (0.5 * bbox_width))
    raw_max_y = int(bbox_center_y + (0.5 * bbox_height))

with open(corrected_bbox_path, 'r', encoding='UTF8') as bbox_txt:
    bbox_data = bbox_txt.read().split()
    
    bbox_center_x = float(bbox_data[1]) * res_width
    bbox_center_y = float(bbox_data[2]) * res_height
    bbox_width = float(bbox_data[3]) * res_width
    bbox_height = float(bbox_data[4]) * res_height

    corrected_min_x = int(bbox_center_x - (0.5 * bbox_width))
    corrected_min_y = int(bbox_center_y - (0.5 * bbox_height))

    corrected_max_x = int(bbox_center_x + (0.5 * bbox_width))
    corrected_max_y = int(bbox_center_y + (0.5 * bbox_height))

raw_img = cv.imread(raw_img_path)
corrected_img = cv.imread(corrected_img_path)

cv.rectangle(raw_img, (raw_min_x, raw_min_y), (raw_max_x, raw_max_y), (0, 0, 255), 1)
cv.rectangle(raw_img, (corrected_min_x, corrected_min_y), (corrected_max_x, corrected_max_y), (0, 255, 0), 1)

cv.rectangle(corrected_img, (raw_min_x, raw_min_y), (raw_max_x, raw_max_y), (0, 0, 255), 1)
cv.rectangle(corrected_img, (corrected_min_x, corrected_min_y), (corrected_max_x, corrected_max_y), (0, 255, 0), 1)

cv.imwrite(save_path + "raw.png", raw_img)
cv.imwrite(save_path + "corrected.png", corrected_img)

#cv.imshow("Raw Image " + str(image_no), img)

#cv.waitKey(0)