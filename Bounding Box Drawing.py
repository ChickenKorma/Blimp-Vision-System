import cv2 as cv
import csv

csv_path_prefix = "D:/Uni Stuff/IP/Data/CSVs/"
img_path_prefix = "D:/Uni Stuff/IP/Data/Images/sphere_cube_"

no_images = 1

cropped_padding = 5
cropped_scale = 5

with open(csv_path_prefix + "boundary boxes.csv", 'r', encoding='UTF8', newline='') as bbox_csv:
    bbox_reader = csv.reader(bbox_csv, delimiter=',')
    next(bbox_reader, None) # skip header row

    min_x = []
    min_y = []
    max_x = []
    max_y = []

    for row in bbox_reader:
        min_x.append(int(row[0]))
        min_y.append(int(row[1]))
        max_x.append(int(row[2]))
        max_y.append(int(row[3]))

for i in range(no_images):
    img = cv.imread(img_path_prefix + str(i) + ".png")
    
    cropped_img = img[(min_y[i] - cropped_padding) : (max_y[i] + cropped_padding), (min_x[i] - cropped_padding) : (max_x[i] + cropped_padding)]

    scaled_width = int(cropped_img.shape[1] * cropped_scale)
    scaled_height = int(cropped_img.shape[0] * cropped_scale)

    cropped_img = cv.resize(cropped_img, (scaled_width, scaled_height), interpolation = cv.INTER_AREA)
    cv.imshow("Cropped image " + str(i), cropped_img)

    cv.rectangle(img, (min_x[i], min_y[i]), (max_x[i], max_y[i]), (0, 255, 0), 1)
    cv.imshow("Bounding box of image " + str(i), img)

cv.waitKey(0)