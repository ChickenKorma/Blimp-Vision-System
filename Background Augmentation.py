

import cv2 as cv
import numpy as np
from sklearn.model_selection import train_test_split

data_path_prefix = "D:/Uni Stuff/IP/Data/"

load_path = data_path_prefix + "Augmented Backgrounds/background_"

train_save_path = data_path_prefix + "YOLO Data/train/images/background_"
val_save_path = data_path_prefix + "YOLO Data/valid/images/background_"
test_save_path = data_path_prefix + "YOLO Data/test/images/background_"

background_images = 627

background_numbers = np.array([])

for image_no in range(background_images):
    for i in range(4):
        number = str(image_no) + "_" + str(i)
        background_numbers = np.append(background_numbers, [number])

train_valid, test = train_test_split(background_numbers, test_size=377)
train, valid = train_test_split(train_valid, test_size=377)

del background_numbers
del train_valid

for num in train:
    image = cv.imread(load_path + num + ".png")
    cv.imwrite(train_save_path + num + ".png", image)

print("Train done")

for num in valid:
    image = cv.imread(load_path + num + ".png")
    cv.imwrite(val_save_path + num + ".png", image)

print("Valid done")

for num in test:
    image = cv.imread(load_path + num + ".png")
    cv.imwrite(test_save_path + num + ".png", image)

print("Test done")