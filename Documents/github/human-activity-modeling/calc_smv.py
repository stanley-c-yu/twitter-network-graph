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
		X1 = None; Y1 = None; Z1 = None; X2 = None; Y2 = None; Z2 = None;
		X3 = None; Y3 = None; Z3 = None; X4 = None; Y4 = None; Z4 = None;
		X5 = None; Y5 = None; Z5 = None; X6 = None; Y6 = None; Z6 = None;
		X7 = None; Y7 = None; Z7 = None;
		variables = [X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3, X4, Y4, Z4, X5, Y5, Z5, X6, Y6, Z6, X7, Y7, Z7]
		if len(columnnames) == len(variables):
			for i in range(len(columnnames)):
				variables[i] = np.asarray(window[columnnames[i]])
		else:
			return "The number of Column Names is not equal to the number of Variables."
		vectors = [variables[i:i + 3] for i in range(0, len(variables), 3)]
		return vectors

	def pdiagnostics(self, window):
		vectors = self.preprocess(window)
		print("\n---------------------------------------------------------------------------------------")
		print("Checking triplet-partitioned vector... ")
		print("Does the partitioned list of vectors have seven nested lists ?", len(vectors) == 7)
		print("\tLength of list: ", len(vectors))
		print("Does a single sublist have a length of three? ", len(vectors[0]) == 3)
		print("\tLength of a single sublist: ", len(vectors[0]))
		print("Checking if the first set of triplets matches the first three accel values in windows...")
		print("\tX1 matching? ", all(vectors[0][0] == np.asarray(window["X1"])))
		print("\tY1 matching? ", all(vectors[0][1] == np.asarray(window["Y1"])))
		print("\tZ1 matching? ", all(vectors[0][2] == np.asarray(window["Z1"])))
		print("Checking if the last set of triplets matches the last three accel values in windows...")
		print("\tX7 matching? ", all(vectors[6][0] == np.asarray(window["X7"])))
		print("\tY7 matching? ", all(vectors[6][1] == np.asarray(window["Y7"])))
		print("\tZ7 matching? ", all(vectors[6][2] == np.asarray(window["Z7"])))
		print("----------------------------------------------------------------------------------------")

	def calcSMV(self, window):
		'''
		Calculates the SMV for each triplet of XYZ accel data for a single 12 sec window.

		Input: A window of 12 sec duration containing seven sets of XYZ triplets of accel data.
		Returns: An array and or df of seven SMV's for each of the seven original triplets,
		possibly with time stamps appended to the front as first column.
		'''
		# timestamps = window["TIME_STAMPS"]
		vectors = self.preprocess(window)
		smv_list = []
		for i in vectors:
		    smv = np.sqrt(np.square(i[0]) + np.square(i[1]) + np.square(i[2]))
		    smv_list.append(smv)
		data = {"SMV1":smv_list[0], "SMV2":smv_list[1], "SMV3":smv_list[2], "SMV4":smv_list[3],
		"SMV5":smv_list[4], "SMV6":smv_list[5], "SMV7":smv_list[6]}
		smv_df = pd.DataFrame(data)
		return smv_df

	def calcAvgSMV(self, window):
		'''
		Calculates the AVG SMV for each of the seven SMV's of a single 12 sec window.

		Input:  A dataframe of seven SMV's from a single 12 sec window or the window itself.
		Returns: A dataframe of seven Average SMV's (scalars, not vecs) for a single 12 sec window.
		'''
		smv_df = self.calcSMV(window)
		smv_arr = np.asarray(smv_df)
		averages = []
		for i in range(0,7):
			avg = np.average(smv_arr[:,i])
			averages.append(avg)
		# print(np.shape(averages))
		# print(averages)
		return averages

	def calcSDevSMV(self, window):
		'''
		Calculates the SD SMV for each of the seven SMV's of a single 12 sec window.

		Input: A dataframe of a single 12 sec window.
		Returns: A list of seven Std. Dev. SMV's (scalars, not vecs) for a single 12 sec window.
		'''
		smv_df = self.calcSMV(window)
		smv_arr = np.asarray(smv_df)
		std_devs = []
		for i in range(0,7):
			sd = np.std(smv_arr[:,i])
			std_devs.append(sd)
		# print(np.shape(std_devs))
		# print(std_devs)
		return std_devs
