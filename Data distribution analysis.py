import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

data_path_prefix = "D:/Uni Stuff/IP/Data/"

#bbox_data = pd.read_csv(data_path_prefix + "bbox data.csv")
pose_data = pd.read_csv(data_path_prefix + "blimp poses.csv")

rot_x = pose_data["rot_x"].to_numpy() 
rot_y = pose_data["rot_y"].to_numpy()
rot_z = pose_data["rot_z"].to_numpy()


#plt.xlabel("Width ($pixels$)")
#plt.ylabel("Height ($pixels$)")
#plt.xticks([0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 1920])
#plt.yticks([0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1080])
#plt.colorbar()
#plt.show()

#bins = 10

#hist_data, edges = np.histogramdd((pos_x, pos_y, pos_z), bins=bins, density=False)

#del pos_x
#del pos_y
#del pos_z

#x = []
#y = []
#z = []
#c = []

#for i in range(bins):
    #start_x = edges[0][i]
    #end_x = edges[0][i+1]
    
    #for j in range(bins):
        #start_y = edges[1][j]
        #end_y = edges[1][j+1]
        
        #for k in range(bins):
            #start_z = edges[2][k]
            #end_z = edges[2][k+1]

            #x.append((start_x + end_x) / 2)
            #y.append((start_y + end_y) / 2)
            #z.append((start_z + end_z) / 2)

            #c.append(hist_data[i][j][k])

plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(rot_x, rot_y, rot_z, alpha=0.2, marker=".")

ax.set_xlim(-0.18, 0.18)
ax.set_ylim(-0.79, 0.79)
ax.set_zlim(-3.15, 3.15)

ax.set_xlabel("X ($rad$)")
ax.set_ylabel("Y ($rad$)")
ax.set_zlabel("Z ($rad$)")
plt.show()