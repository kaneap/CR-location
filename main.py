import warnings

import cv2 as cv2
import matplotlib.pyplot as plt
import numpy as np

warnings.simplefilter("ignore")
pi = np.pi
plt.rcParams["figure.figsize"] = 15, 17

# Next define the pixel to meter ratio, scanner resolution and a function to plot the robot in the map.
px_size = 0.04  # in m
pxpm = 1 / px_size
scannerres = 2  # in degree
max_range = 12  # in m

robot_radius = 12  # approximation from picture, in pixels

#  this function plots a visualization of the robot
#  pose has to be [x,y,theta], c is the color as string (e.g. "steelblue")


def plotRobotPose(pose, c="steelblue"):
    plt.plot(
        [pose[1], pose[1] + 18 * np.sin(np.deg2rad(pose[2]))],
        # 18 pixels is just the length of the heading direction line (no deeper meaning)
        [pose[0], pose[0] + 18 * np.cos(np.deg2rad(pose[2]))],
        color="black",
        linewidth=3.5,
    )
    circle = plt.Circle(
        (pose[1], pose[0]),
        robot_radius,
        facecolor=c,
        linewidth=3.5,
        edgecolor="black",
        fill=True,
    )
    plt.gcf().gca().add_artist(circle)


# this one handles lines in the 45° cones along the x-axis
# pose = robot pose, slope = ray you want to check, m = map,
# img = map where you want to draw the scans in
def linehigh(pose, slope, m):
    max_range_in_pixels = max_range / 0.04
    number_of_pixels_walked = 0
    current_col_index = float(pose[1])
    col_step_size = float(slope[0]) / float(slope[1]) if slope[1] != 0 else 0.0
    row_step_direction = -1 if pose[0] > row2index else 1
    print(str(pose[0]) + ' - ' + str(row2index))
    for current_row_index in range(pose[0], row2index, row_step_direction):
        number_of_pixels_walked += 1
        if m[current_row_index][int(round(current_col_index))] != 255.0:
            m[current_row_index][int(round(current_col_index))] = 250.0
        else:
            break
        col_step_direction = 1 if pose[1] < col2index else -1
        current_col_index += abs(col_step_size) * col_step_direction
        if number_of_pixels_walked == max_range_in_pixels:
            break


# and this one deals with the two remaining cones along the y-axis
def linelow(pose, slope, m):
    max_range_in_pixels = max_range / 0.04
    number_of_pixels_walked = 0
    current_row_index = float(pose[0])
    row_step_size = float(slope[1]) / float(slope[0]) if slope[0] != 0 else 0.0
    column_step_direction = -1 if pose[1] > col2index else 1
    for currentColIndex in range(pose[1], col2index, column_step_direction):
        number_of_pixels_walked += 1
        if m[int(round(current_row_index))][currentColIndex] != 255.0:
            m[int(round(current_row_index))][currentColIndex] = 250.0
        else:
            break
        row_step_direction = 1 if pose[0] < row2index else -1
        current_row_index += abs(row_step_size) * row_step_direction
        if number_of_pixels_walked == max_range_in_pixels:
            break
    


def line(pose, slope, m):
    if abs(slope[1]) < abs(slope[0]):
        return linelow(pose, slope, m)
    else:
        return linehigh(pose, slope, m)


# get the map
m = cv2.imread("Assignment_04_Grid_Map.png", 0)
# trim off the weird right side of the image
m = m[:, :678]
# and adjust it to our preferred values
m = np.ones_like(m) * 255 - m

# set the pose to the following values [x,y,theta], where positive x
# is downwards in image coordinates, positive y is to the right
# the results are output as angles in [0,360) so it is recommended to supply them in that format


# please use this pose for the scanning and for the endpoint model in task 4.2
pose = np.array([215, 375, 240])
startDegree = pose[2] - 125
endDegree = pose[2] + 126
for slope in range(startDegree,endDegree,scannerres): #range(240-125, 240+126, 2):
    row2index = pose[0] + int(np.cos(slope * np.pi / 180.0) * (1200 / 4))
    col2index = pose[1] + int(np.sin(slope * np.pi / 180.0) * (1200 / 4))
    diff_row_index = pose[0] - row2index
    diff_col_index = pose[1] - col2index
    line(pose, [diff_col_index, diff_row_index], m)

# display the map and the pose
plt.imshow(m, cmap="gray_r")
plotRobotPose(pose, "red")
plt.savefig("test.png")
plt.show()
