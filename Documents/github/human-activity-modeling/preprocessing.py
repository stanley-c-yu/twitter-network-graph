#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:20:03 2020

@author: stanley-yu
"""
# Import dependencies 
import pandas as pd
import numpy as np
import glob
import math 
from tqdm import tqdm
from pandasql import sqldf
from datetime import datetime  
from datetime import timedelta  
pysqldf = lambda q: sqldf(q, globals()) 

class preprocessor:
    
    def __init__(self, sensor_data, ground_truth_data):
        self.sensor_data = sensor_data
        self.ground_truth_data = ground_truth_data
        
    
    def filterSensor(self):
        ''' 
        Filters a sensor data frame to observations that fall within the bounds of gound truths. 
        '''
        lower_bound = self.ground_truth_data["START_TIME"].min()
        upper_bound = self.ground_truth_data["STOP_TIME"].max() 
        query = "SELECT * FROM sensor_one WHERE HEADER_TIME_STAMP BETWEEN '" + lower_bound + "' AND '" + upper_bound + "'"
        filteredSensor = pysqldf(query)
        return filteredSensor 
    
    def divideIntoTwelveDotEights(self): 
        '''
        Divides the filtered sensor data into windows of 12.8s duration.  
        '''
        filteredSensor = self.filterSensor()
        filteredSensor["HEADER_TIME_STAMP"] = pd.to_datetime(filteredSensor["HEADER_TIME_STAMP"])
        time_stamps = [] 
        lower_bound = pd.to_datetime(self.ground_truth_data["START_TIME"].min())
        upper_bound = pd.to_datetime(self.ground_truth_data["STOP_TIME"].max())
        marker = lower_bound
        while marker < upper_bound:
            marker = marker + timedelta(seconds = 12.8)
            time_stamps.append(marker)
        doce_octo_windows = [] 
        for i in range(len(time_stamps)):
            bound1 = str(time_stamps[i])
            j = i + 1 
            if j == len(time_stamps): 
                break
            else: 
                bound2 = str(time_stamps[j])
                tmp = filteredSensor[(filteredSensor["HEADER_TIME_STAMP"] >= bound1) & (filteredSensor["HEADER_TIME_STAMP"] <= bound2)]
                doce_octo_windows.append(tmp)
        return doce_octo_windows
    
    def trimIntoTwelves(self): 
        ''' 
        Trims the first and last 0.4 seconds off of the 12.8s windows and returns a list of 12s window dataframes.
        '''
        doce_octo_windows = self.divideIntoTwelveDotEights() 
        doce_windows = []
        for i in doce_octo_windows: 
            lower_bound = i["HEADER_TIME_STAMP"].min() + timedelta(seconds = 0.4)
            upper_bound = i["HEADER_TIME_STAMP"].max() - timedelta(seconds = 0.4)
            tmp = i[(i["HEADER_TIME_STAMP"] >= lower_bound) & (i["HEADER_TIME_STAMP"] <= upper_bound)]
            doce_windows.append(tmp)
        return doce_windows 
            
    def divideIntoSubWindows(self, window): 
        '''
        Helper method to splitAllWindows that takes each 12s window and divides into a list of 6 2sec dataframes. 
        '''
        time_stamps = [] 
        lower_bound = window["HEADER_TIME_STAMP"].min() 
        upper_bound = window["HEADER_TIME_STAMP"].max()
        marker = lower_bound 
        while marker < upper_bound: 
            marker = marker + timedelta(seconds = 2)
            time_stamps.append(marker)
        six_two_sec_intervals = [] 
        for i in range(len(time_stamps)):
            bound1 = time_stamps[i]
            j = i + 1
            if j == len(time_stamps):
                break
            else:
                bound2 = time_stamps[j]
                tmp = window[(window["HEADER_TIME_STAMP"] >= bound1) & (window["HEADER_TIME_STAMP"] <= bound2)]
                six_two_sec_intervals.append(tmp)
        return six_two_sec_intervals
    
    def splitAllWindows(self): 
        '''
        Splits each window into a list of 6 two-sec duration dataframes.  
        '''
        doce_windows = self.trimIntoTwelves()
        all_sub_windows = [] 
        for i in doce_windows: 
            six_two_sec_intervals = self.divideIntoSubWindows(i)
            all_sub_windows.append(six_two_sec_intervals)
        return all_sub_windows 
    
    def calcSMV(self, window, printout = False, counter = None):         
        '''
        Helper method that calculates the Signla Mag. Vector, the SMV Average, and SMV Std. Dev. over a 12sec window.
        '''
        X = np.asarray(window["X_ACCELERATION_METERS_PER_SECOND_SQUARED"])
        Y = np.asarray(window["Y_ACCELERATION_METERS_PER_SECOND_SQUARED"])
        Z = np.asarray(window["Z_ACCELERATION_METERS_PER_SECOND_SQUARED"])
        smv = np.sqrt(np.square(X) + np.square(Y) + np.square(Z))
        smv_avg = np.mean(smv)
        smv_sd = np.std(smv)
        if printout == True: 
            print("SMV Mean over 12s window number ", counter, ": ", smv_avg, ".  SMV SD over 12s window number", counter, ": ", smv_sd, ".")
        return smv, smv_avg, smv_sd 
    
    def calcAllSMV(self, printout = False): 
        ''' 
        Calculates the Signal Mag. Vec., SMV Avg. and SMV Std. Dev. for all 12 sec windows.  
        '''
        doce_windows = self.trimIntoTwelves()
        smv_list = [] 
        smv_means = [] 
        smv_sds = []
        counter = 1
        for window in doce_windows:
            smv, smv_avg, smv_sd = self.calcSMV(window, printout, counter)
            smv_list.append(smv)
            smv_means.append(smv_avg)
            smv_sds.append(smv_sds)
            counter += 1
        return smv_list, smv_means, smv_sds
    
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


# filteredData = filterSensor(sensor_one, ground_truths)
# filteredData.head()

# Read in data 
file_prefix = "muss_data/SPADES_1/MasterSynced/2015/09/24/14/"

# filenames = ["ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-09-24-14-23-00-000-M0400.sensor.csv", 
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv", 
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150085-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150108-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150126-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
#             "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150175-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
#              "SPADESInLab.diego-SPADESInLab.2015-09-24-14-35-07-891-M0400.annotation.csv"
#             ]

filepaths = [file for file in glob.glob(file_prefix + "*.csv")]
datasets = []
for filepath in tqdm(filepaths): 
    tmp = pd.read_csv(filepath)
    datasets.append(tmp)
    
# Print filepaths 
# for i in filepaths: 
#     print(i)

# Read in one sensor file and the ground truths
sensor_one = datasets[0]
ground_truths = datasets[5]


## Test Cases  
prc = preprocessor(sensor_data = sensor_one, ground_truth_data = ground_truths)
twelveDotEights = prc.divideIntoTwelveDotEights()
twelves = prc.trimIntoTwelves()
allSubWindows = prc.splitAllWindows()
smvList, smvAvgList, smvSDList = prc.calcAllSMV(printout = True)