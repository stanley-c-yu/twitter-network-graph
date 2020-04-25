import pandas as pd 
import numpy as np 

class calculateSMV: 

	def preprocess(self, window): 
		'''
		Helper method that takes a single window and breaks it down into triplets of XYZ in list of lists.  

		Input: Window, a 12sec duration dataframe with Time Stamps and seven triplets of XYZ accelermeter data.  
		Returns: A list of lists, where each nested list is a triplet of XYZ accelerometer data from one of 
`		seven actigraph sensors.  
		'''
		columnnames = window.columns[1:]
        	variables = [X1 = None, Y1 = None, Z1 = None, X2 = None, Y2 = None, Z2 = None,
        	X3 = None, Y3 = None, Z3 = None, X4 = None, Y4 = None, Z4 = None,
        	X5 = None, Y5 = None, Z5 = None, X6 = None, Y6 = None, Z6 = None,
        	X7 = None, Y7 = None, Z7 = None]	
		if len(columnnames) == len(variables): 
			for i in range(len(columnnames): 
				variables[i] = np.asarray(window[columnnames[i]])
		else: 
			return "The number of Column Names is not equal to the number of Variables." 
		vectors = []		
		for i in variables: 
			counter = 1
			triplet = [] 
			while counter<4: 
				triplet.append(variables[i])
				counter += 1 
			vectors.append(triplet) 
		return vectors
		
		 	
		
