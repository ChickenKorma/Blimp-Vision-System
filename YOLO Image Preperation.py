import numpy as np

bbox_path_prefix = "D:/Uni Stuff/IP/Data/Bounding Boxes/image_"

total_images = 15000

def valid(value):
    return value >= 0 and value <= 1

for image_no in range(total_images):
    with open(bbox_path_prefix + str(image_no) + ".txt", "r", encoding="UTF8") as bbox_data:
        elements = bbox_data.read().split()

    centre_x = float(elements[1])
    centre_y = float(elements[2])
    width = float(elements[3])
    height = float(elements[4])

    max_x = centre_x + (width / 2)
    min_x = centre_x - (width / 2)

    max_y = centre_y + (height / 2)
    min_y = centre_y - (height / 2)

    if valid(max_x) and valid(min_x) and valid(max_y) and valid(min_y):
        continue

    if not valid(max_x):
        #print(str(image_no) + " is too wide right")
        max_x = np.clip(max_x, 0.0, 1.0)

    if not valid(min_x):
        #print(str(image_no) + " is too wide left")
        min_x = np.clip(min_x, 0.0, 1.0)

    if not valid(max_y):
        #print(str(image_no) + " is too high bottom")
        max_y = np.clip(max_y, 0.0, 1.0)

    if not valid(min_y):
        #print(str(image_no) + " is too high top")
        min_y = np.clip(min_y, 0.0, 1.0)

    centre_x = (max_x + min_x) / 2
    centre_y = (max_y + min_y) / 2

    width = max_x - min_x
    height = max_y - min_y

    with open(bbox_path_prefix + str(image_no) + ".txt", "w", encoding="UTF8") as bbox_data:
        bbox_data.write("0 " + str(centre_x) + " " + str(centre_y) + " " + str(width) + " " + str(height))

    print("Cropped image_" + str(image_no))