import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt
import numpy.linalg as la
import time
import warnings
warnings.simplefilter("ignore")
pi = np.pi
plt.rcParams['figure.figsize'] = 15, 17

#Next define the pixel to meter ratio, scanner resolution and a function to plot the robot in the map.
px_size = 0.04 # in m
pxpm = 1/px_size
scannerres = 2 # in degree
max_range = 12 # in m

robot_radius = 12 # approximation from picture, in pixels

### this function plots a visualization of the robot
### pose has to be [x,y,theta], c is the color as string (e.g. "steelblue")
def plotRobotPose(pose, c = "steelblue"):
    plt.plot([pose[1], pose[1] + 18*np.sin(np.deg2rad(pose[2]))], # 18 pixels is just the length of the heading direction line (no deeper meaning)
             [pose[0] , pose[0] + 18*np.cos(np.deg2rad(pose[2]))], 
                color= "black", linewidth = 3.5)
    circle=plt.Circle((pose[1],pose[0]),robot_radius,facecolor=c, linewidth = 3.5, edgecolor = "black",fill=True)
    plt.gcf().gca().add_artist(circle)

###this one handles lines in the 45° cones along the x-axis
# pose = robot pose, slope = ray you want to check, m = map, 
# img = map where you want to draw the scans in
def linelow(pose, slope, m, img):
    k = 0.
    return k

###and this one deals with the two remaining cones along the y-axis
def linehigh(pose, slope, m, img):
    k = 0.
    return k

def line(pose, slope, m, img):
    if abs(slope[1]) < abs(slope[0]):
            return linelow(pose, slope, m,img)
    else:
            return linehigh(pose, slope, m,img)

###get the map
m = cv2.imread("Assignment_04_Grid_Map.png", 0)
###trim off the weird right side of the image
m = m[:,:678]
###and adjust it to our preferred values
m = np.ones_like(m)*255 - m

###set the pose to the following values [x,y,theta], where positive x 
###is downwards in image coordinates, positive y is to the right
###the results are output as angles in [0,360) so it is recommended to supply them in that format

###please use this pose for the scanning and for the endpoint model in task 4.2
pose = np.array([215,375,240])

###display the map and the pose
plt.imshow(m, cmap = "gray_r")
plotRobotPose(pose,'red')
plt.show()