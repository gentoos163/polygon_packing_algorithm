import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


def interpolate_coordinates(coordinates_xy: list):
    arr = np.array(coordinates_xy)
    x, y = zip(*arr)
    #in this specific instance, append an endpoint to the starting point to create a closed shape
    x = np.r_[x, x[0]]
    y = np.r_[y, y[0]]
    #create spline function
    f, u = interpolate.splprep([x, y], s=0, per=True)
    #create interpolated lists of points
    xint, yint = interpolate.splev(np.linspace(0, 1, 50), f)
    return np.column_stack((xint, yint))


