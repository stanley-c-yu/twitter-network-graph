from to_numpy import toNumpyArray
from orientation_angles import orientationAngles
import numpy as np

class orientationFeatures:

    def __init__(self, filteredSensor, ground_truths):
        self.filteredSensor = filteredSensor
        self.ground_truths = ground_truths

    def captureRepresentativeOrientation(self, window_np_orientation_angles):
        '''
        Calculates the Representative Orientation across all subwindows of a single window, and returns a numpy array of the
        median for each X, Y, Z orientation angle vector.
        '''
        medians = []
        medians.append(np.median(window_np_orientation_angles[:,0])) # X vector of orientation angles
        medians.append(np.median(window_np_orientation_angles[:,1])) # Y
        medians.append(np.median(window_np_orientation_angles[:,2])) # Z
        rep_orientations = np.asarray(medians)
        return rep_orientations

    def captureOrientationChange(self, window_np_orientation_angles):
        '''
        Calculates the orientation change across all subwindows of a single window, and returns a numpy array of the
        range for each X, Y, Z orientation angle vector.
        '''
        maximums = []
        minimums = []
        maximums.append(np.nanmax(window_np_orientation_angles[:,0])) # X vector of orientation angles
        maximums.append(np.nanmax(window_np_orientation_angles[:,1])) # Y vector of orientation angles
        maximums.append(np.nanmax(window_np_orientation_angles[:,2])) # Z vector of orientation angles
        minimums.append(np.nanmin(window_np_orientation_angles[:,0])) # X
        minimums.append(np.nanmin(window_np_orientation_angles[:,1])) # Y
        minimums.append(np.nanmin(window_np_orientation_angles[:,2])) # Z
        orietnation_change = np.asarray(maximums) - np.ararray(minimums)
        return orientation_change

    def computeOrientationFeatures(self):
        '''
        Calculates and returns the orientation features for all windows.
        '''
        grouped_orientation_arrays = {}
        oa = orientationAngles(self.filteredSensor, self.ground_truths)
        window_orientation_angles = oa.calcAllOrientationAngles()
        for window in window_orientation_angles.keys():
            window_np_orientation_angles = toNumpyArray(window_orientation_angles[window])
            grouped_orientation_arrays[window] = window_np_orientation_angles
        grouped_orientation_features = {}
        for window in grouped_orientation_arrays.keys():
            orientation_change = self.captureOrientationChange(grouped_orientation_arrays[window])
            rep_orientation = self.captureRepresentativeOrientation(grouped_orientation_arrays[window])
            grouped_orientation_features[window] = list(orientation_change, rep_orientation)
        return grouped_orientation_arrays
