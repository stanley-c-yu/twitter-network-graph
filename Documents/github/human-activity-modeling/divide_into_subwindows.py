from divide_into_windows import windowDivisor
import pandas as pd
from datetime import timedelta

class subWindowDivisor:

    def __init__(self, focused_macro_sensor, ground_truths, ts_col_name):
        self.focused_macro_sensor = focused_macro_sensor
        self.ground_truths = ground_truths
        self.col_name = ts_col_name

    def divideIntoSubWindows(self, window):
        '''
        Helper method to splitAllWindows that takes each 12s window and divides into a list of 6 2sec dataframes.
        '''
        time_stamps = []
        lower_bound = window[self.col_name].min()
        upper_bound = window[self.col_name].max()
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
                tmp = window[(window[self.col_name] >= bound1) & (window[self.col_name] <= bound2)]
                six_two_sec_intervals.append(tmp)
        return six_two_sec_intervals

    def splitAllWindows(self):
        '''
        Splits each window into a list of 6 two-sec duration dataframes.
        '''
        wd = windowDivisor(self.focused_macro_sensor, self.ground_truths, self.col_name)
        doce_windows = wd.trimIntoTwelves()
        all_sub_windows = []
        for i in doce_windows:
            six_two_sec_intervals = self.divideIntoSubWindows(i)
            all_sub_windows.append(six_two_sec_intervals)
        return all_sub_windows
