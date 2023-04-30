import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

data_path_prefix = "D:/Uni Stuff/IP/Data/"

with np.load(data_path_prefix + "Generation Times.npz", allow_pickle=True) as times:
    render_times = times["render"]
    pose_times = times["pose"]
    bbox_times = times["bbox"]

total_times = np.add(render_times, pose_times)
del render_times
del pose_times

total_times = np.add(total_times, bbox_times)
del bbox_times

#print(np.min(total_times))
#print(np.max(total_times))
#print(np.mean(total_times))

plt.hist(total_times, bins=50)
plt.xlabel("Total generation time per image ($s$)")
plt.ylabel("Frequency")
plt.show()