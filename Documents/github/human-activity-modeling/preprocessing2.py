#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 17:15:48 2020

@author: stanley-yu
"""

from load_files import fileLoader
import pandas as pd 
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())
import numpy as np
from divide_into_windows import windowDivisor
from divide_into_subwindows import subWindowDivisor
#from signal_magnitude_vector import calculateSMV

## Read in data  --------------------------------------------------------------------------------------------------------- ##

file_prefix = "muss_data/SPADES_1/MasterSynced/2015/09/24/14/"

file_names = ["ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150066-AccelerationCalibrated.2015-09-24-14-23-00-000-M0400.sensor.csv", 
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150075-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv", 
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150084-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150085-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150108-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150126-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv",
            "ActigraphGT9X-AccelerationCalibrated-NA.TAS1E23150175-AccelerationCalibrated.2015-09-24-14-18-00-000-M0400.sensor.csv"
            ]
gt_filename = "SPADESInLab.diego-SPADESInLab.2015-09-24-14-35-07-891-M0400.annotation.csv"

# Read in the data
fl = fileLoader() 
ground_truths, loaded = fl.load_files(file_prefix, file_names, gt_filename)
fl.diagnostics(ground_truths, loaded, file_names)

# Extracting sensor data to variable names
sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7 = loaded[0], loaded[1], loaded[2], loaded[3], loaded[4], loaded[5], loaded[6]

## Create a super dataframe by merging all the accelerometer values togehter --------------------------------------------- ##
# Join sensor 1 to sensor 2 
tmp = sensor1.join(sensor2, lsuffix= '_s1', rsuffix = '_s2')
tmp = tmp.iloc[:, [0,1,2,3,5,6,7]]
column_names = tmp.columns 
tmp = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1", 
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2"}, axis = 1)
# Join sensor 3
tmp = tmp.join(sensor3, lsuffix = '_call', rsuffix = '_other')
tmp = tmp.iloc[:, [0,1,2,3,4,5,6,8,9,10]]   
column_names = tmp.columns 
tmp = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1",
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2", column_names[7]:"X3", 
                           column_names[8]:"Y3", column_names[9]:"Z3"}, axis = 1)              
# Join sensor 4
tmp = tmp.join(sensor4, lsuffix = '_call', rsuffix = '_other')
tmp = tmp.iloc[:,[0,1,2,3,4,5,6,7,8,9,11,12,13]]
column_names = tmp.columns
tmp  = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1",
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2", column_names[7]:"X3", 
                           column_names[8]:"Y3", column_names[9]:"Z3", column_names[10]: "X4", column_names[11]:"Y4",
                           column_names[12]:"Z4"}, axis = 1)    
# Join sensor 5 
tmp = tmp.join(sensor5, lsuffix = '_call', rsuffix = '_other')
tmp = tmp.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,14,15,16]]
column_names = tmp.columns
tmp  = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1",
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2", column_names[7]:"X3", 
                           column_names[8]:"Y3", column_names[9]:"Z3", column_names[10]: "X4", column_names[11]:"Y4",
                           column_names[12]:"Z4", column_names[13]:"X5", column_names[14]:"Y5", column_names[15]:"Z5"},
                  axis = 1)    
# Join sensor 6 
tmp = tmp.join(sensor6, lsuffix = '_call', rsuffix = '_other')
tmp = tmp.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19]]
column_names = tmp.columns
tmp  = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1",
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2", column_names[7]:"X3", 
                           column_names[8]:"Y3", column_names[9]:"Z3", column_names[10]: "X4", column_names[11]:"Y4",
                           column_names[12]:"Z4", column_names[13]:"X5", column_names[14]:"Y5", column_names[15]:"Z5", 
                           column_names[16]:"X6", column_names[17]:"Y6", column_names[18]:"Z6"},
                  axis = 1)   
# Join sensor 7 
tmp = tmp.join(sensor7, lsuffix = '_call', rsuffix = '_other')
tmp = tmp.iloc[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,22]]
column_names = tmp.columns
macro_sensor  = tmp.rename(mapper = {column_names[0]:"TIME_STAMPS", column_names[1]:"X1", column_names[2]:"Y1", column_names[3]:"Z1",
                           column_names[4]:"X2", column_names[5]:"Y2", column_names[6]:"Z2", column_names[7]:"X3", 
                           column_names[8]:"Y3", column_names[9]:"Z3", column_names[10]: "X4", column_names[11]:"Y4",
                           column_names[12]:"Z4", column_names[13]:"X5", column_names[14]:"Y5", column_names[15]:"Z5", 
                           column_names[16]:"X6", column_names[17]:"Y6", column_names[18]:"Z6", column_names[19]:"X7", 
                           column_names[20]:"Y7", column_names[21]:"Z7"},
                  axis = 1)   

## Filter the dataframe down to observations that fall within the bounds of the ground truths ----------------------------##
lower_bound = ground_truths['START_TIME'].min()
upper_bound = ground_truths['STOP_TIME'].max()
query = "SELECT * FROM macro_sensor WHERE TIME_STAMPS BETWEEN '" + lower_bound + "' AND '" + upper_bound + "'"
focused_macro_sensor = pysqldf(query)

## Divide the Focused Macro-Sensor DF into Windows of 12 second Duration -------------------------------------------------##
wd = windowDivisor(focused_macro_sensor, ground_truths, "TIME_STAMPS")
twelve_sec_windows = wd.trimIntoTwelves() 
# Last DF is empty, so let's trim it.  
twelve_sec_windows = twelve_sec_windows[0:114]

## Divide the 12sec windows of the Focused Macro-Sensor DF into 2s sub-windows -------------------------------------------##
swd = subWindowDivisor(focused_macro_sensor, ground_truths, "TIME_STAMPS")
two_sec_swindows = swd.splitAllWindows()

## Calculate Signal Magnitude Vector features for each 12sec window ------------------------------------------------------##
from calc_smv import calculateSMV
csmv = calculateSMV()
partitions = csmv.preprocess(twelve_sec_windows[0])
csmv.pdiagnostics(twelve_sec_windows[0])
smv_df = csmv.calcSMV(twelve_sec_windows[0])
averages = csmv.calcAvgSMV(twelve_sec_windows[0])
std_devs = csmv.calcSDevSMV(twelve_sec_windows[0])

## Calculate All Average SMV's (for all windows)
all_avgs = []
for window in twelve_sec_windows:
    avgs = csmv.calcAvgSMV(window)
    all_avgs.append(avgs)
all_avgs = np.asarray(all_avgs) 

print("\n-----------------------------------------------------------------------------------------------")
print("Running Diagnostics on 'Complete' SMV Averages array: ")
nrows, ncols = np.shape(all_avgs)
print("Dimensions of Averages Array: ", np.shape(all_avgs))
print("Number of 12 sec windows: ", len(twelve_sec_windows))
print("There should be as many rows of SMV averages as there are windows, i.e., one window has a set of seven smv averages.")
print("\tIs there a set of SMV Averages for each window? ", len(twelve_sec_windows) == nrows)
print("------------------------------------------------------------------------------------------------")

## Calculate All Std. Dev. SMV's (for all windows)
all_stdvs = [] 
for window in twelve_sec_windows: 
    std_devs = csmv.calcSDevSMV(window)
    all_stdvs.append(std_devs)
all_stdvs = np.asarray(all_stdvs)

print("\n-----------------------------------------------------------------------------------------------")
print("Running Diagnostics on 'Complete' SMV Std. Dev.'s array: ")
nrows, ncols = np.shape(all_stdvs)
print("Dimensions of Std. Dev's Array: ", np.shape(all_stdvs))
print("Number of 12 sec windows: ", len(twelve_sec_windows))
print("There should be as many rows of SMV std. dev.'s as there are windows, i.e., one window has a set of seven smv std. dev.'s.")
print("\tIs there a set of SMV Std. Dev.'s for each window? ", len(twelve_sec_windows) == nrows)
print("------------------------------------------------------------------------------------------------")    

## Combine SMV-based features to get an array of Motion Features 1
motion_features = np.hstack((all_avgs, all_stdvs))
print("Motion features dimensions: ", np.shape(motion_features))

# Isolate time stamps 
time_stamps = [] 
for window in twelve_sec_windows: 
    ts = window["TIME_STAMPS"].iloc[0]
    time_stamps.append(ts)
time_stamps = np.asarray(time_stamps)
print("Time Stamps array for windows of Motion Features Dimensions: ", np.shape(time_stamps))

# Incorporate time_stamps into motion features array
time_stamps = np.reshape(time_stamps, (114,1))
motion_features = np.hstack((time_stamps, motion_features))
print("The dimensions of the motion features dataset with time stamps: ", np.shape(motion_features))

# Merge labels from Ground Truths
ground_truths["HEADER_TIME_STAMP"] = pd.to_datetime(ground_truths["HEADER_TIME_STAMP"])
ground_truths["START_TIME"] = pd.to_datetime(ground_truths["START_TIME"])
ground_truths["STOP_TIME"] = pd.to_datetime(ground_truths["STOP_TIME"])

motion_features = pd.DataFrame(motion_features, columns = ["TIME_STAMPS", "SMV_Avg1", "SMV_Avg2", "SMV_Avg3", "SMV_Avg4", 
                                                           "SMV_Avg5", "SMV_Avg6", "SMV_Avg7", 
                                                           "SMV_Std_Dev1", "SMV_Std_Dev2", "SMV_Std_Dev3", 
                                                           "SMV_Std_Dev4","SMV_Std_Dev5", "SMV_Std_Dev6", "SMV_Std_Dev7"])

packed = list(zip(ground_truths.START_TIME, ground_truths.STOP_TIME, ground_truths.LABEL_NAME))
motion_features["LABELS"] = [[ev for strt, end, ev in packed if strt <= el <= end] for el in motion_features.TIME_STAMPS]

dataset = pd.DataFrame(
    [[t,val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,e] for t, val1, val2, val3, val4, val5, 
     val6, val7, val8, val9, val10, val11, val12, val13, val14, event in zip(motion_features.TIME_STAMPS, 
                                                                             motion_features.SMV_Avg1, 
                                                                             motion_features.SMV_Avg2,
                                                                             motion_features.SMV_Avg3,
                                                                             motion_features.SMV_Avg4, 
                                                                             motion_features.SMV_Avg5, 
                                                                             motion_features.SMV_Avg6, 
                                                                             motion_features.SMV_Avg7,
                  motion_features.SMV_Std_Dev1, motion_features.SMV_Std_Dev2, motion_features.SMV_Std_Dev3,
                  motion_features.SMV_Std_Dev4,motion_features.SMV_Std_Dev5,motion_features.SMV_Std_Dev6,
                  motion_features.SMV_Std_Dev7, motion_features.LABELS) for e in event], columns=motion_features.columns)

dataset.to_csv("fulldata.csv", index=False)