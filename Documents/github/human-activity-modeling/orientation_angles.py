from divide_into_subwindows import subWindowDivisor
from to_dictionary import toDictionary
import math
import numpy as np
import pandas as pd

class orientationAngles:

    def __init__(self, filteredSensor, ground_truths):
        self.filteredSensor = filteredSensor
        self.ground_truths = ground_truths

    def calcOrientAngles(self, subwindow, printout = False, reshape = True):
        '''
        Helper method that calculates the orientation angles of a single 2-second subwindow.
        '''
        # Isolate X, Y, and Z accelerometer vectors
        swX = subwindow['X_ACCELERATION_METERS_PER_SECOND_SQUARED']
        swY = subwindow['Y_ACCELERATION_METERS_PER_SECOND_SQUARED']
        swZ = subwindow['Z_ACCELERATION_METERS_PER_SECOND_SQUARED']
        # Calculate average of the X, Y, and Z  vectors from the subwindow.
        mean_accel_x = np.mean(np.asarray(swX))
        mean_accel_y = np.mean(np.asarray(swY))
        mean_accel_z = np.mean(np.asarray(swZ))
        if printout == True:
            print("Mean Acceleration Value of X: ", round(mean_accel_x, 4), " | Mean Acceleration Value of Y: ", round(mean_accel_y, 4),
                  " | Mean Acceleration Value of Z: ", round(mean_accel_z, 4))
        # Calculate the approximate orient vector
        approx_orient_vec = [mean_accel_x, mean_accel_y, mean_accel_z]
        approx_orient_vec = np.asarray(approx_orient_vec)
        if reshape == True:
            approx_orient_vec = np.reshape(approx_orient_vec, (3,1))
        if printout == True:
            print(approx_orient_vec)
            print("Dimensions: ", np.shape(approx_orient_vec))
        # Calculate denominator for normalization of approx. orientation vector
        denominator = math.sqrt(mean_accel_x**2 + mean_accel_y**2 + mean_accel_z**2)
        # Normalize Approximated Orientation Vector
        normalized_aov = approx_orient_vec/denominator
        if printout == True:
            print(normalized_aov)
            print("Length of vector: ", np.linalg.norm(normalized_aov))
        # Calculate the orientation angles
        orient_angles = np.arccos(normalized_aov)
        if printout == True:
            print(orient_angles)
        return orient_angles

    def calcAllOrientationAngles(self):
        '''
        Calculates the orientation angles for all subwindows in each window.
        Returns a dictionary of window-keys with orientation-angle vectors as list-values.
        '''
        window_orientation_angles = {}
        swd = subWindowDivisor(self.filteredSensor, self.ground_truths)
        all_sub_windows = swd.splitAllWindows()
        window_dictionary = toDictionary(all_sub_windows)
        for window in sorted(window_dictionary.keys()):
            orientation_angles = []
            for subwindow in window_dictionary[window]:
                oa = calcOrientAngles(subwindow)
                orientation_angles.append(oa)
            window_orientation_angles[window] = orientation_angles
        return window_orientation_angles
