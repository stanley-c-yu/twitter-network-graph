# Import dependencies
import pandas as pd
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

def filterSensor(sensor_data, ground_truths):
    '''
    Filters a sensor data frame to observations that fall within the bounds of ground truths.
    '''
    lower_bound = ground_truths['START_TIME'].min()
    upper_bound = ground_truths['STOP_TIME'].max()
    query = "SELECT * FROM sensor_data WHERE HEADER_TIME_STAMP BETWEEN '" + lower_bound + "' AND '" + upper_bound + "'"
    filteredSensor = pysqldf(query)
    return filteredSensor

# How to import:
# from filter_data import filterSensor
