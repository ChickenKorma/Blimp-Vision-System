import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

data_path_prefix = "D:/Uni Stuff/IP/Data/"

with np.load(data_path_prefix + "Correction Times.npz", allow_pickle=True) as times:
    time = times["bbox_undistortion_times"]

#total_times = np.add(image_undistortion_times, bbox_undistortion_times)

#print(np.min(bbox_undistortion_times))
#print(np.max(bbox_undistortion_times))
#print(np.mean(bbox_undistortion_times))

print((time.size - np.count_nonzero(time)) / time.size)

plt.hist(time, bins=50, range=[0,0.04])
plt.xlabel("Bounding box generation time per image ($s$)")
plt.ylabel("Frequency")
#plt.show()