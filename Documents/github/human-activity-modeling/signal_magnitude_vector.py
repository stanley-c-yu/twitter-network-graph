from divide_into_windows import windowDivisor
import numpy as np
import pandas as pd

class calculateSMV:
    '''
    Calculates the Signal Magnitude Vector (SMV) and SMV-related features for each
    12-sec window.
    '''

    def __init__(self, focused_macro_sensor, ground_truths, ts_col_name):
        self.focused_macro_sensor = focused_macro_sensor
        self.ground_truths = ground_truths
        self.col_name = ts_col_name

    def calcSMV(self, window, printout = False, counter = None):
        '''
        Helper method that calculates the Signla Mag. Vector, the SMV Average, and SMV Std. Dev. over a 12sec window.
        '''
        X1 = np.asarray(window["X1"])
        Y1 = np.asarray(window["Y1"])
        Z1 = np.asarray(window["Z1"])
        X2 = np.asarray(window["X2"])
        Y2 = np.asarray(window["Y2"])
        Z2 = np.asarray(window["Z2"])
        X3 = np.asarray(window["X3"])
        Y3 = np.asarray(window["Y3"])
        Z3 = np.asarray(window["Z3"])
        X4 = np.asarray(window["X4"])
        Y4 = np.asarray(window["Y4"])
        Z4 = np.asarray(window["Z4"])
        X5 = np.asarray(window["X5"])
        Y5 = np.asarray(window["Y5"])
        Z5 = np.asarray(window["Z5"])
        X6 = np.asarray(window["X6"])
        Y6 = np.asarray(window["Y6"])
        Z6 = np.asarray(window["Z6"])
        X7 = np.asarray(window["X7"])
        Y7 = np.asarray(window["Y7"])
        Z7 = np.asarray(window["Z7"])
        vectors = [[X1, Y1, Z1], [X2, Y2, Z2], [X3, Y3, Z3], [X4, Z4, Y4], [X5, Z5, Y5], [X6, Y6, Z6], [X7, Y7, Z7]]
        smv_list = []
        for i in vectors:
            smv = np.sqrt(np.square(i[0]) + np.square(i[1]) + np.square(i[2]))
            smv_list.append(smv)
        smv_averages = []
        for i in smv_list:
            smv_avg = np.mean(i)
            smv_averages.append(smv_avg)
        smv_std_devs = []
        for i in smv_list:
            smv_sd = np.std(i)
            smv_std_devs.append(smv_sd)
        if printout == True:
            print("SMV Mean over 12s window number ", counter, ": ", smv_avg, ".  SMV SD over 12s window number", counter, ": ", smv_sd, ".")
        return smv_list, smv_averages, smv_std_devs

    def calcAllSMV(self, printout = False):
        '''
        Calculates the Signal Mag. Vec., SMV Avg. and SMV Std. Dev. for all 12 sec windows.
        '''
        wd = windowDivisor(self.focused_macro_sensor, self.ground_truths, self.col_name)
        doce_windows = wd.trimIntoTwelves()
        smv_list = []
        smv_means = []
        smv_sds = []
        counter = 1
        for window in doce_windows:
            smvs, smv_avgs, smv_sds = self.calcSMV(window, printout, counter)
            smv_list.append(smvs)
            smv_means.append(smv_avgs)
            smv_sds.append(smv_sds)
            counter += 1
        # smv_means_df = pd.DataFrame(smv_means, columns = ["SMV Mean 1", "SMV Mean 2", "SMV Mean 3", "SMV Mean 4",
        # "SMV Mean 5", "SMV Mean 6", "SMV Mean 7"])
        # smv_std_devs_df = pd.DataFrame(smv_sds, columns = ["SMV SD 1", "SMV SD 2", "SMV SD 3", "SMV SD 4", "SMV SD 5",
        # "SMV SD 6", "SMV SD 7"])
        return smv_list, smv_means, smv_sds
