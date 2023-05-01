import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

data_path_prefix = "D:/Uni Stuff/IP/Data/"

with np.load(data_path_prefix + "Correction Times.npz", allow_pickle=True) as times:
    image_undistortion_times = times["image_undistortion_times"]
    bbox_undistortion_times = times["bbox_undistortion_times"]

total_times = np.add(image_undistortion_times, bbox_undistortion_times)

#print(np.min(bbox_undistortion_times))
#print(np.max(bbox_undistortion_times))
#print(np.mean(bbox_undistortion_times))

plt.hist(total_times, bins=50)
plt.xlabel("Total undistortion time per image ($s$)")
plt.ylabel("Frequency")
plt.show()