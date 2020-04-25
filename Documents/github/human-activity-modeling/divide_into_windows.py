# Import dependencies
import pandas as pd
from datetime import timedelta

class windowDivisor:
    '''Divides a sensor data frame into a list of 12 second duration windows.'''

    def __init__(self, focused_macro_sensor, ground_truths, ts_col_name):
        self.focused_macro_sensor = focused_macro_sensor
        self.ground_truths = ground_truths
        self.col_name = ts_col_name

    def divideIntoTwelveDotEights(self):
        '''
        Divides the filtered sensor data into windows of 12.8s duration.
        Returns a list of 12.8s length dataframes.
        '''
        self.focused_macro_sensor[self.col_name] = pd.to_datetime(self.focused_macro_sensor[self.col_name])
        time_stamps = []
        lower_bound = pd.to_datetime(self.ground_truths["START_TIME"].min())
        upper_bound = pd.to_datetime(self.ground_truths["STOP_TIME"].max())
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
                tmp = self.focused_macro_sensor[(self.focused_macro_sensor[self.col_name] >= bound1) & (self.focused_macro_sensor[self.col_name] <= bound2)]
                doce_octo_windows.append(tmp)
        return doce_octo_windows

    def trimIntoTwelves(self):
        '''
        Trims the first and last 0.4 seconds off of the 12.8s windows and returns a list of 12s window dataframes.
        '''
        doce_octo_windows = self.divideIntoTwelveDotEights()
        doce_windows = []
        for i in doce_octo_windows:
            lower_bound = i[self.col_name].min() + timedelta(seconds = 0.4)
            upper_bound = i[self.col_name].max() - timedelta(seconds = 0.4)
            tmp = i[(i[self.col_name] >= lower_bound) & (i[self.col_name] <= upper_bound)]
            doce_windows.append(tmp)
        return doce_windows
