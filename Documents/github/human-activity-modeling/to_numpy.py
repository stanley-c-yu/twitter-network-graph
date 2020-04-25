import numpy as np

def toNumpyArray(window_orientation_angles):
    '''
    Takes a dictionary of window orientation angles (key = window, value = list of orientation angle vectors
    from each subwindow) and turns it into a dictionary of numpy arrays (key = window, value = numpy array of
    the orientation angles from each subwindow).

    Array should be returned in X, Y, Z order.
    '''
    window_np_orientation_angles = {}
    for window in sorted(window_orientation_angles.keys()):
        window_np_orientation_angles[window] = np.stack(window_orientation_angles[window], axis = 0)
    return window_np_orientation_angles
