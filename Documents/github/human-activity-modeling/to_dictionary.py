def toDictionary(all_sub_windows):
'''Takes a list of subwindow dataframes and puts them in a dictionary format. '''
    window_dictionary = {}
    keys = []
    for i in range(len(all_sub_windows)):
        keys.append("Window" + str(i))
    for i in range(len(all_sub_windows)):
        window_dictionary[keys[i]] = all_sub_windows[i]
    return window_dictionary
# How to import:
# from to_dictionary import toDictionary    
