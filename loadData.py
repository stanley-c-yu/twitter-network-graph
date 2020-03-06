import pandas as pd
import numpy as np

class loadData: 
	def __init__(self): 
		self.prefix = "data/twitter/"

	def load_file(self, filepath): 
		dataframe = pd.read_csv(filepath, header = None, delim_whitespace = True, encoding = "ISO-8859-1")
		return dataframe.values 

	def load_group(self, filenames): 
		loaded = list()
		for name in filenames: 
			data = self.load_file(self.prefix + name)
			loaded.append(data)
		return loaded 




