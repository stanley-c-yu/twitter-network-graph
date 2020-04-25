#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:04:21 2020

@author: stanley-yu
"""
import pandas as pd
import numpy as np
from tqdm import tqdm

class fileLoader: 
    
    
    def load_files(self, file_prefix, file_names, ground_truth_file_name):
        '''
        Parameters
        ----------
        file_prefix : STRING
            Up stream filepath. 
        file_names : String
            Downstream filepath
        ground_truth_file_name : String
            Up stream filepath. 
    
        Returns
        -------
        ground_truths : Pandas Dataframe
            A dataframe of the activity labels for each observed activity. 
        loaded : List
            List of Pandas dataframes containing accelerometer data from each sensor used.
    
        '''
        ground_truths = pd.read_csv(file_prefix + ground_truth_file_name)
    
        filepaths = []
        for file in file_names: 
            filepath = file_prefix + file
            filepaths.append(filepath) 
        
        loaded = [] 
        for filepath in tqdm(filepaths): 
            data = pd.read_csv(filepath)
            data["HEADER_TIME_STAMP"] = pd.to_datetime(data["HEADER_TIME_STAMP"]) # Convert key columns to datetime
            loaded.append(data)
        
        return ground_truths, loaded 
        
    def diagnostics(self, ground_truths, loaded, file_names):
        print("Printing meta data on imported data: ")
        print("Does 'loaded' have the same number files as indicated in 'filenames'? ", len(loaded) == len(file_names))
        print("\n \t 'loaded' has ", len(loaded), "dataframes inside of it.")
        print("\nColumns of a single sensor dataframe: \n", list(loaded[0].columns))
        print("\n\tShape of a single sensor dataframe, including time stamps: \n\t", np.shape(loaded[0]))
        print("\nColumns of the ground truth dataframe: \n", list(ground_truths.columns))
        print("\n\tShape of the ground truth dataframe: \n\t", np.shape(ground_truths))